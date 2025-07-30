from app import celery
from models.models import User
from utils.email import send_email
from datetime import datetime
from flask import current_app

@celery.task
def send_daily_reminders():
    with current_app.app_context():
        users = User.query.all()
        for user in users:
            subject = "⏰ Parking Reminder - Book Your Slot Today!"
            body = f"Hi {user.fullname},\n\nDon't forget to reserve your parking spot for today if needed.\n\n- ParkEasy Team"
            send_email(user.email, subject, body)
