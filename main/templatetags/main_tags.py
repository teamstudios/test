from django import template
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings

from goods.models import WishList
from accounts.models import Subscribers
from accounts.constants import FACEBOOK, PINTEREST, VK
from chat.models import Thread

register = template.Library()


@register.filter()
def add_class_to_formfield(field, css):
    """
    Added css class to form field.
    """
    return field.as_widget(attrs={"class": css})


@register.filter()
def add_placeholder_to_field(field, text):
    """

    :param field:
    :param text:
    :return:
    """
    field.field.widget.attrs.update({'placeholder':text})
    return field


@register.filter()
def check_http_prefix(siteaddr):
    """
    If siteaddr doesn't have http or https prefix - add it
    :param siteaddr - string with web url
    :return string
    """
    if siteaddr is not None:
        if siteaddr.startswith("http") or siteaddr.startswith("https"):
            return siteaddr
        else:
            return "http://" + siteaddr


@register.filter()
def show_count_goods_in_wishlist(user):
    """
    Show number of goods in user;s wishlist
    :param user: User object
    :return: str
    """
    if user.is_authenticated():
        try:
            count = user.wishlist.goods.count()
            return "<span>" + str(count) + "</span>"
        except WishList.DoesNotExist:
            pass
    return ""


@register.filter()
def show_count_subscriptions(user):
    """
    Show number of users, on which this user is sibscribed
    :param user: User object
    :return: str
    """
    if user.is_authenticated():
        try:
            count = user.subscribers.users.count()
            return count
        except Subscribers.DoesNotExist:
            pass
    return 0


@register.filter()
def show_unread_message_count(user):
    """
    Shown number of unread messages
    :param user: User object
    :return: str
    """
    if user.is_authenticated():
        try:
            count = user.threads.filter(has_unread=True).count()
            if count != 0:
                return "<span>" + str(count) + "</span>"
        except Thread.DoesNotExist:
            pass
    return ""


@register.filter()
def social_share(link, network):
    """
    Return link to sharing in social network
    :param link: link to share
    :param network: socia network to share
    :return: str
    """
    if network == FACEBOOK:
        share_link = "https://www.facebook.com/sharer/sharer.php?u={link}".format(link=link)
    elif network == VK:
        share_link = "http://vk.com/share.php?url={link}".format(link=link)
    elif network == PINTEREST:
        share_link = "https://pinterest.com/pin/create/button/?url={link}&media={file}&description={desc}".format(
            link=link,
            file=static(settings.NO_GOOD),
            desc="Sell and Buy"
        )
    else:
        share_link = "{link}".format(link=link)
    return share_link
