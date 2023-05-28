import os
import smtplib
import ssl
from email.mime.text import MIMEText


def send_email(email, subject, text):
    from_ = os.getenv('HELP_EMAIL')
    to_ = [email]
    content = MIMEText(text)
    content['Subject'] = subject

    context = ssl.create_default_context()
    with smtplib.SMTP(os.getenv('SMTP_SITE'), int(os.getenv('SMTP_PORT'))) as server:
        server.starttls(context=context)
        server.login(os.getenv('HELP_EMAIL'), os.getenv('HELP_PASSWORD'))
        server.sendmail(from_, to_, content.as_string())

    return True
