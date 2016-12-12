from django import template

from chat.functions import check_user_in_blocklist


register = template.Library()


@register.filter()
def check_user_in_blocklist_tag(sender, partner):
    return check_user_in_blocklist(sender, partner)