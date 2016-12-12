from django.contrib.sites.shortcuts import get_current_site
from django.utils.functional import SimpleLazyObject


def get_site(request):
    """
    Add site and site root to context processors
    :param request: HttpRequest
    :return: dict
    """
    site = SimpleLazyObject(lambda: get_current_site(request))
    protocol = 'https' if request.is_secure() else 'http'
    return {
        'site': site.domain,
        'site_root': SimpleLazyObject(lambda : "{0}://{1}".format(protocol, site.domain))
    }