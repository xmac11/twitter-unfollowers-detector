import logging
import smtplib
from email.message import EmailMessage

from constants.config import FROM_ADDRESS, TO_ADDRESS, SMTP_HOST, SMTP_PORT
from constants.emails import SCRIPT_RESULTS, SUCCESSFUL_UNFOLLOW_MSG, UNSUCCESSFUL_UNFOLLOW_MSG, NO_ACTION_NEEDED_MSG
from constants.secrets import EMAIL_PASSWORD
from utils.format import format_message
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


def send_email_with_results(*, success_user_ids, error_user_ids, no_need_to_unfollow_ids):
    if not any([*success_user_ids, *error_user_ids, *no_need_to_unfollow_ids]):
        return

    success_msg = format_message(message=SUCCESSFUL_UNFOLLOW_MSG, user_ids=success_user_ids)
    error_msg = format_message(message=UNSUCCESSFUL_UNFOLLOW_MSG, user_ids=error_user_ids)
    no_action_needed_msg = format_message(message=NO_ACTION_NEEDED_MSG, user_ids=no_need_to_unfollow_ids)

    content = f'{success_msg}\n{error_msg}\n{no_action_needed_msg}'
    send_email(subject=SCRIPT_RESULTS, content=content)
