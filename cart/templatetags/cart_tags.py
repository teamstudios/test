from django import template

from cart.cart import Cart
from cart.models import AuctionCartModel

register = template.Library()


@register.simple_tag(takes_context=True)
def show_carts_count(context):
    """
    Shown number of items in cart
    :param context: RequestContext object
    :return: str
    """
    if context.request.user.is_authenticated():
        cart = Cart(context.request)
        count = len(cart.cart.items())
        return str(count)
    else:
        return ""


@register.filter()
def show_good_bid(good, username):
    """
    Wrapper tag for calling get_last_bid method
    :param good: Good object
    :param username: username (str)
    :return: Decimal or None
    """
    return good.get_last_bid(username)


@register.filter()
def check_accepted_bid(good, username):
    """
    Wrapper tag for calling check_accepted_bid method
    :param good: Good object
    :param username: username (str)
    :return: Bool
    """
    return good.check_accepted_bid(username)


@register.simple_tag(takes_context=True)
def show_showcase_count(context):
    """
    Show number of user's goods in other users carts
    :param context: RequestContext object
    :return: str
    """
    if context.request.user.is_authenticated():
        carts = AuctionCartModel.objects.filter(good__user=context.request.user).count()
        return str(carts)
    else:
        return ""
