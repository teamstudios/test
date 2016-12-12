from django import template


register = template.Library()


@register.filter()
def get_mark_count_about(profile, mark):
    return profile.get_mark_count_about(mark)