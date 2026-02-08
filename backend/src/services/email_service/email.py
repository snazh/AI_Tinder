import smtplib

from src.config import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

SMTP_SERVER = "smtp.gmail.com"
SMTP_PORT = 587


def send_email(receiver_email, subject, body):
    try:
        msg = MIMEMultipart()
        msg['From'] = settings.email_client.EMAIL_ADDRESS
        msg['To'] = receiver_email
        msg['subject'] = subject
        msg.attach(MIMEText(body, 'plain'))
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(settings.email_client.EMAIL_ADDRESS, settings.email_client.EMAIL_PASSWORD)
            server.sendmail(settings.email_client.EMAIL_ADDRESS, receiver_email, msg.as_string())
        print("Email sent")
    except Exception as e:
        print(f"Email error occurred: {e}")
