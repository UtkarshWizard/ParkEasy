import csv
import os
from datetime import datetime , timezone
from models.models import Reservation, User
from app import celery
from utils.email import send_email

EXPORT_FOLDER = "exports"  # Make sure this folder exists or create it dynamically

@celery.task
def generate_csv_report(user_id):
    user = User.query.get(user_id)
    if not user:
        return

    reservations = Reservation.query.filter_by(user_id=user_id).all()

    if not reservations:
        return

    filename = f"{EXPORT_FOLDER}/parking_history_{user.id}_{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}.csv"
    os.makedirs(EXPORT_FOLDER, exist_ok=True)

    with open(filename, mode='w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["Reservation ID", "Slot ID", "Spot ID", "Entry Time", "Exit Time", "Cost"])
        for r in reservations:
            writer.writerow([
                r.id,
                r.spot.lot_id,
                r.spot.id,
                r.parking_timestamp.strftime('%Y-%m-%d %H:%M'),
                r.leaving_timestamp.strftime('%Y-%m-%d %H:%M') if r.leaving_timestamp else "",
                r.parking_cost
            ])

    subject = "Your Parking History Export is Ready"
    body = f"""
        Hello {user.fullname},

        Your parking history has been generated and is attached as a CSV file.

        If you have any questions, feel free to contact us.

        Regards,  
        ParkEasy Team
    """

    html_body = f"""
        <p>Hello {user.fullname},</p>
        <p>Your parking history has been generated successfully and is attached below as a CSV file.</p>
        <p><strong>Filename:</strong> {os.path.basename(filename)}</p>
        <p>Thank you for using ParkEasy!</p>
    """

    send_email( user.email, subject, body=body , html_body=html_body , attachment_path=filename)
