from smtplib import SMTP
from os import getenv

SMTP_HOST = getenv('SMTP_HOST', 'localhost')
SMTP_PORT = int(getenv('SMTP_PORT', '25'))
SMTP_SENDER = getenv('SMTP_SENDER', 'sender@example.com')
SMTP_FROM = getenv('SMTP_FROM', 'Send Er <sender@example.com>')

CONFIRMATION_LINK_BASE = getenv('CONFIRMATION_LINK_BASE', 'https://example.com/confirm')

def send_confirmation_email(email: str, first_name: str, last_name: str) -> bool:
    """Arguments passed to this function should be checked elsewhere."""
    # TODO: implement generation of random and mostly unpredictable key
    random_key = '12345678'

    # TODO: think about what should be in message body
    message = f"""From: {SMTP_FROM}
To: {email}
Subject: Registration Confirmation

Please confirm your registration to receive your number by clicking on this link: {CONFIRMATION_LINK_BASE}?key={random_key}
"""

    # TODO: handle exceptions here
    mail_server = SMTP(SMTP_HOST, SMTP_PORT)
    mail_server.sendmail(SMTP_SENDER, email, message)
    mail_server.close()

    return True
