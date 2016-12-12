import requests
import hashlib
import logging
from storesb.settings import SMSAERO_URL, SMSAERO_LOGIN, SMSAERO_PASSWORD, SMSAERO_RESPONSE_FORMAT, SMSAERO_GROUP
from celery.task import task

from main.functions import send_user_notification


log = logging.getLogger(__name__)


@task(name='send-api-request-task')
def send_api_request_task(phone_number, text):
    """
    TASK for send request to sms message on SMS aero. Logs result in logfile.
    :param phone_number: Number to send
    :param text: Text to send
    """
    params = {
        'user': SMSAERO_LOGIN,
        'password': hashlib.md5(SMSAERO_PASSWORD.encode('utf-8')).hexdigest(),
        'to': phone_number,
        'text': text,
        'answer': SMSAERO_RESPONSE_FORMAT,
        'from': SMSAERO_GROUP,
    }
    response = requests.get(SMSAERO_URL, params=params)
    # Convert result to json
    response_as_json = response.json()
    if response_as_json['result'] == 'accepted':
        log_string = "Result {result}, id {id}".format(result=response_as_json['result'], id=response_as_json['id'])
        log.debug(log_string)
    else:
        log_string = "Result {result}".format(result=response_as_json['result'])
        log.error(log_string)


@task(name='send-email-task')
def send_email_task(subject, notification, from_email, to_email):
    """
    Task for send email to user. And log result of operation.
    :param subject: Email subject
    :param notification: Email text
    :param from_email: sender email
    :param to_email: receiver email
    :return: None
    """
    try:
        send_user_notification(subject, notification, from_email, to_email)
        log_string = "Email was sent to {email}. Subject {subject}".format(email=to_email, subject=subject)
        log.debug(log_string)
    except Exception:
        log_string = "Failed to send email to {email}. Subject {subject}".format(email=to_email, subject=subject)
        log.error(log_string)