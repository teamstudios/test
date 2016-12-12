from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from common.decorators import ajax_required
from goods.models import Good
from goods.constants import ITEMS_COUNT

from .cart import Cart
from .models import AuctionCartModel

# Create your views here.


@require_POST
@ajax_required
def add_to_cart(request):
    """
    Add good to cart. Accept AJAX request from add_to_cart script.
    :param request: HttpRequest (contains good id)
    :return: JsonResponse
    """
    cart = Cart(request)
    try:
        good = Good.objects.get(id=request.POST.get('id'))
    except Good.DoesNotExist:
        return JsonResponse({'status': 'error', 'reason': 'good not found'})
    cart.add(good)
    return JsonResponse({'status': 'ok'})


@login_required
def cart_detail(request):
    """
    Show goods in user cart.
    :param request: HttpRequest
    :return: HttpResponse; (rendered cart_detail.html template)
    """
    cart = Cart(request)
    goods = [item['good'] for item in cart]
    count = len(goods)
    paginator = Paginator(goods, ITEMS_COUNT)
    page = request.GET.get('page')
    try:
        goods = paginator.page(page)
    except PageNotAnInteger:
        goods = paginator.page(1)
    except EmptyPage:
        goods = paginator.page(paginator.num_pages)
    return render(request, 'cart_detail.html', {'goods': goods, 'count': count})


@require_POST
def remove_from_cart(request):
    """
    Remove good from cart. Accept AJAX request from add_to_cart script.
    :param request: HttpRequest (contains good id)
    :return: JsonResponse
    """
    cart = Cart(request)
    try:
        good = Good.objects.get(id=request.POST.get('id'))
    except Good.DoesNotExist:
        return JsonResponse({'status': 'error', 'reason': 'good not found'})
    cart.remove(good)
    return JsonResponse({'status': 'ok'})


@login_required
def show_showcase(request):
    """
    Show showcase
    :param request: HttpRequest
    :return: HttpResponse (rendered showcase_detal.html template)
    """
    carts = AuctionCartModel.objects.filter(good__user=request.user)
    count = carts.count()
    paginator = Paginator(carts, ITEMS_COUNT)
    page = request.GET.get('page')
    try:
        carts = paginator.page(page)
    except PageNotAnInteger:
        carts = paginator.page(1)
    except EmptyPage:
        carts = paginator.page(paginator.num_pages)
    return render(request, "showcase_detal.html", {"carts": carts, 'count': count})
