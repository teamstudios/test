from .constants import VK, FACEBOOK, PINTEREST


def accounts_processor(request):
    """
    Context processor
    Return constants that used in templates
    :param request: HttpRequest
    :return: dict
    """
    return {"VK": VK, "FACEBOOK": FACEBOOK, "PINTEREST": PINTEREST}
