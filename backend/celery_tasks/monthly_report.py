from app import celery
from models.models import db, Reservation, User, ParkingLot
from flask import render_template_string
from datetime import datetime, timezone
from utils.email import send_email

@celery.task
def send_monthly_report():
    users = User.query.all()
    current_month = datetime.now(timezone.utc).month
    current_year = datetime.now(timezone.utc).year

    for user in users:
        reservations = Reservation.query.filter(
            Reservation.user_id == user.id,
            db.extract('month', Reservation.parking_timestamp) == current_month,
            db.extract('year', Reservation.leaving_timestamp) == current_year
        ).all()

        if not reservations:
            continue

        total_cost = sum([r.parking_cost for r in reservations])
        lot_usage = {}
        for r in reservations:
            lot = r.spot.lot.location_name
            lot_usage[lot] = lot_usage.get(lot, 0) + 1

        most_used_lot = max(lot_usage, key=lot_usage.get) if lot_usage else "N/A"

        body = f"""
            Hello {user.fullname},

            Your monthly parking report has been generated.

            If you have any questions, feel free to contact us.

            Regards,  
            ParkEasy Team
        """

        html_content = render_template_string("""
        <h2>Monthly Parking Report - {{ month }} {{ year }}</h2>
        <p>Hello {{ name }},</p>
        <p>Here's your parking activity report for this month:</p>
        <ul>
            <li><strong>Total Bookings:</strong> {{ total }}</li>
            <li><strong>Most Used Parking Lot:</strong> {{ lot }}</li>
            <li><strong>Total Amount Spent:</strong> ₹{{ cost }}</li>
        </ul>
        <p>Thank you for using ParkEasy!</p>
        """, name=user.fullname, month=datetime.now(timezone.utc).strftime("%B"),
             year=current_year, total=len(reservations),
             lot=most_used_lot, cost=total_cost)

        send_email(
            recipient=user.email,
            subject="Your Monthly Parking Report",
            body=body,
            html_body=html_content
        )
