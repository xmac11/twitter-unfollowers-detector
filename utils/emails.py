import logging
import os
import smtplib
from email.message import EmailMessage

from constants.emails import FROM_ADDRESS, TO_ADDRESS, SMTP_HOST, SMTP_PORT
from constants.logs import FORMAT, DATE_FORMAT
from settings import LOGS_ROOT

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

file_handler = logging.FileHandler(os.path.join(LOGS_ROOT, 'emails.log'))

formatter = logging.Formatter(FORMAT, DATE_FORMAT)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)


def send_email(content):
    msg = EmailMessage()
    msg['Subject'] = 'Problem with twitter-unfollowers script'
    msg['From'] = FROM_ADDRESS
    msg['To'] = TO_ADDRESS
    msg.set_content(content)

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        try:
            password = os.environ['EMAIL_PASSWORD']
            smtp.login(FROM_ADDRESS, password)
            smtp.send_message(msg)
        except Exception as e:
            logger.exception(e)
