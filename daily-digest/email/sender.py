import smtplib
import logging
from email.message import EmailMessage
from ..env import *

logger = logging.getLogger(__name__)


def send_email(to: str, subject: str, body: str):
    
    # Connect to the SMTP server
    logger.info(f"Connecting to SMTP server: {SMTP_SERVER}:{SMTP_PORT}")
    smtp = smtplib.SMTP(host=SMTP_SERVER, port=int(SMTP_PORT))
    smtp.ehlo()
    smtp.starttls()
    smtp.login(SMTP_USERNAME, SMTP_PASSWORD)
    
    # Create the email
    msg = EmailMessage()
    msg.set_content(body)
    msg["Subject"] = subject
    msg["From"] = SMTP_USERNAME
    msg["To"] = to
    
    # Send the email
    logger.info("Sending email")
    smtp.send_message(msg)
    smtp.quit()
    