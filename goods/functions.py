from django.db.models import Q
from .models import Good

from common.functions import convert_str_to_float


def simple_search(words, tags=None):
    """
    Perform simple search (QuerySet API __icontains) on tags in tags field and on string in title or properties_description field.
    :param words: String
    :param tags: List of Tags(taggit.models Tag). Optional parameter
    :return: QuerySet of found goods
    """
    if tags:
        goods = Good.active.filter(Q(tags__in=tags) | Q(title__icontains=words) | Q(properties__description__icontains=words)).distinct().order_by('-created')
    else:
        goods = Good.active.filter(Q(title__icontains=words) | Q(properties__description__icontains=words)).distinct().order_by('-created')
    return goods


def filtered_search(request_method):
    """
    Perform the filter by criteria
    :param request_method: request.GET or request.POST
    :return: Goods queryset
    """
    all_goods = Good.active.all()
    if 'name' in request_method:
        all_goods = all_goods.filter(title__icontains=request_method['name'])
    if 'max_cost' in request_method:
        max_cost = convert_str_to_float(request_method['max_cost'])
        all_goods = all_goods.filter(Q(old_price__lte=max_cost) | Q(new_price__lte=max_cost) |
                                     Q(price__lte=max_cost) | Q(min_price__lte=max_cost) |
                                     Q(reserve_price__lte=max_cost) | Q(max_price__lte=max_cost))
    if 'min_cost' in request_method:
        min_cost = convert_str_to_float(request_method['min_cost'])
        all_goods = all_goods.filter(Q(old_price__gte=min_cost) | Q(new_price__gte=min_cost) |
                                     Q(price__gte=min_cost) | Q(min_price__gte=min_cost) |
                                     Q(reserve_price__gte=min_cost) | Q(max_price__gte=min_cost))
    if 'location' in request_method:
        all_goods = all_goods.filter(location__icontains=request_method['location'])
    if 'deal' in request_method:
        all_goods = all_goods.filter(deal=request_method['deal'])
    if 'state' in request_method:
        all_goods = all_goods.filter(state=request_method['state'])
    if 'delivery_form' in request_method:
        all_goods = all_goods.filter(delivery_form=request_method['delivery_form'])
    if 'cooperation' in request_method:
        all_goods = all_goods.filter(cooperation__icontains=request_method['cooperation'])
    if 'tag_id[]' in request_method:
        tags_ids = request_method.getlist('tag_id[]')
        all_goods = all_goods.filter(tags__in=tags_ids).distinct()
    if 'trade_mark' in request_method:
        all_goods = all_goods.filter(properties__trade_mark__icontains=request_method['trade_mark'])
    if 'model' in request_method:
        all_goods = all_goods.filter(properties__model__icontains=request_method['model'])
    if 'material' in request_method:
        all_goods = all_goods.filter(properties__material__icontains=request_method['material'])
    if 'size' in request_method:
        all_goods = all_goods.filter(properties__size__icontains=request_method['size'])
    if 'color' in request_method:
        all_goods = all_goods.filter(properties__color__icontains=request_method['color'])
    if 'weight' in request_method:
        weight = convert_str_to_float(request_method['weight'])
        all_goods = all_goods.filter(properties__weight=weight)
    if 'equipment' in request_method:
        all_goods = all_goods.filter(properties__equipment__icontains=request_method['equipment'])
    if 'vendor' in request_method:
        all_goods = all_goods.filter(properties__vendor__icontains=request_method['vendor'])
    return all_goods