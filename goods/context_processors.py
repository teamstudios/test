from .constants import BUY_SELL, SALE, AUCTION, NEW, USED, LOGISTIC, MAIL, COURIER, HANDS, PICKUP
from .constants import TO_BUYER, BY_SELLER, MONETARY, REPLACEMENT


def const_processor(request):
    """
    Context processor
    Return constants^ that used in templates
    :param request: HttpRequest
    :return: dict
    """
    return {'BUY_SELL': BUY_SELL, 'SALE': SALE, 'AUCTION': AUCTION, 'NEW': NEW, 'USED': USED, 'LOGISTIC': LOGISTIC,
            'MAIL': MAIL, 'COURIER': COURIER, 'HANDS': HANDS, 'PICKUP': PICKUP, 'TO_BUYER': TO_BUYER,
            'BY_SELLER': BY_SELLER, 'MONETARY': MONETARY, 'REPLACEMENT': REPLACEMENT}