import logging
import smtplib
from email.message import EmailMessage

from constants.config import FROM_ADDRESS, TO_ADDRESS, SMTP_HOST, SMTP_PORT
from constants.emails import SUCCESSFUL_UNFOLLOW, UNSUCCESSFUL_UNFOLLOW
from constants.secrets import EMAIL_PASSWORD
from utils.format import format_link_by_user_id
from utils.logging import setup_logger

logger = setup_logger(name=__name__, level=logging.ERROR, filename='emails.log')


def send_email(*, subject, content):
    if not all([FROM_ADDRESS, TO_ADDRESS, SMTP_HOST, SMTP_PORT, EMAIL_PASSWORD]):
        return

    msg = EmailMessage()
    msg['From'] = FROM_ADDRESS
    msg['To'] = TO_ADDRESS
    msg['Subject'] = subject
    msg.set_content(content)

    with smtplib.SMTP_SSL(SMTP_HOST, SMTP_PORT) as smtp:
        try:
            smtp.login(FROM_ADDRESS, EMAIL_PASSWORD)
            smtp.send_message(msg)
        except Exception as e:
            logger.exception(e)


def send_email_with_successfully_unfollowed(user_ids):
    send_email_with_results(user_ids, SUCCESSFUL_UNFOLLOW)


def send_email_with_unsuccessfully_unfollowed(user_ids):
    send_email_with_results(user_ids, UNSUCCESSFUL_UNFOLLOW)


def send_email_with_results(user_ids, subject):
    if user_ids:
        content = '\n'.join([format_link_by_user_id(user_id) for user_id in user_ids])
        send_email(subject=subject, content=content)
