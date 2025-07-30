import smtplib
from email.message import EmailMessage
from config import Config as cfg
import mimetypes
import os

def send_email(recipient, subject, body, html_body=None, attachment_path=None):
    msg = EmailMessage()
    msg['From'] = cfg.MAIL_DEFAULT_SENDER
    msg['To'] = recipient
    msg['Subject'] = subject

    msg.set_content(body)
    if html_body:
        msg.add_alternative(html_body, subtype='html')

    if attachment_path and os.path.exists(attachment_path):
        with open(attachment_path, 'rb') as f:
            file_data = f.read()
            file_name = os.path.basename(attachment_path)
            mime_type, _ = mimetypes.guess_type(attachment_path)
            maintype, subtype = (mime_type or 'application/octet-stream').split('/')
            msg.add_attachment(file_data, maintype=maintype, subtype=subtype, filename=file_name)

    with smtplib.SMTP(cfg.MAIL_SERVER, cfg.MAIL_PORT) as smtp:
        smtp.starttls()
        smtp.login(cfg.MAIL_USERNAME, cfg.MAIL_PASSWORD)
        smtp.send_message(msg)
