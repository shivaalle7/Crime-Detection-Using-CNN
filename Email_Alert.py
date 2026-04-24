import smtplib
from email.message import EmailMessage

def send_email_alert(msg):
    email = EmailMessage()
    email['Subject'] = 'Crime Alert Triggered'
    email['From'] = 'yourmail@gmail.com'
    email['To'] = 'admin@gmail.com'
    email.set_content(msg)
    # configure SMTP credentials before use