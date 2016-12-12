from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.core.mail import EmailMultiAlternatives


def send_user_notification(subject, notification, from_email, to_email):
    """
    Send notification to user
    :param subject: Subject of email
    :param notification: Text of notification
    :param from_email: Sender email
    :param to_email: User email
    :return:
    """
    template_html = 'email/notification.html'
    html_content = render_to_string(template_html, {'subject': subject, 'notification': notification})
    text_content = strip_tags(html_content)
    if type(to_email) not in (tuple, list):
        receivers = [to_email]
    else:
        receivers = to_email
    msg = EmailMultiAlternatives(subject, text_content, from_email, receivers)
    msg.attach_alternative(html_content, 'text/html')
    msg.send(fail_silently=False)
