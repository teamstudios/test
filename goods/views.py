import json
from itertools import chain
from decimal import Decimal

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse, HttpResponse
from django.db.models import Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils.text import slugify
from django.core.urlresolvers import reverse, reverse_lazy
from django.contrib import messages
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.views.generic.edit import DeleteView
from django.utils.decorators import method_decorator

from taggit.models import Tag

from common.decorators import ajax_required

from main.forms import SearchForm
from accounts.models import UserProfile
from accounts.constants import NOT_DEFINED
from cart.cart import Cart
from cart.models import AuctionCartModel

from .models import Good, GoodsPhotos, GoodsComments, WishList, GoodsProperties, AuctionBids
from .forms import GoodForm, GoodPropetiesForm, CustomImageUpload
from .functions import simple_search, filtered_search
from .constants import AUCTION, ITEMS_COUNT
from .tasks import post_to_social_network

# Create your views here.


def search_view(request):
    """
    Search view. If 'query' or 'filter' not in request.GET or form is invalid - render index.html.
    Else render  search_categories.html and pass found objects(goods, it's(goods) count and it's sellers(user model).
    If 'filter' in request.Get - perform filtered search
    :param request: HttpRequest with query parameter.
    :return: HttpResponse
    """

    if 'query' in request.GET:
        # Default search by tag or title/description
        form = SearchForm(request.GET)
        if form.is_valid():
            page_id = 'search' # Set page id (to use in template )
            search_request = form.cleaned_data['query']
            tags = []
            for word in search_request.split(' '):
                tags = list(chain(tags, Tag.objects.filter(name__icontains=word)))
            if tags:
                objects = simple_search(search_request, tags)
            else:
                objects = simple_search(search_request)
            objects_count = objects.count()
            # Store query result in session (just id's)
            request.session['query_result'] = json.dumps(list(objects.values_list('id', flat=True)))
        else:
            form = SearchForm()
            return render(request, "index.html", {"theme_id": NOT_DEFINED, 'form': form})
    elif 'filter' in request.GET:
        # Filtered search by filter parameters
        search_request = request.GET.urlencode()
        objects = filtered_search(request.GET)
        objects_count = objects.count()
        page_id = 'filter' # Set page id(to use in template )
        # Store query result in session (just id's)
        request.session['query_result'] = json.dumps(list(objects.values_list('id', flat=True)))
    else:
        form = SearchForm()
        return render(request, "index.html", {"theme_id": NOT_DEFINED, 'form': form})
    sellers = UserProfile.objects.filter(user__goods__in=objects).distinct()[:5]
    paginator = Paginator(objects, ITEMS_COUNT)
    page = request.GET.get('page')
    try:
        objects = paginator.page(page)
    except PageNotAnInteger:
        objects = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        objects = paginator.page(paginator.num_pages)
    form = SearchForm()
    all_tags = Tag.objects.all()
    if request.is_ajax():
        return render(request, 'search_category_ajax.html', {"objects": objects, 'objects_count': objects_count,
                                                             'search_request': search_request,
                                                             'sellers': sellers, 'form': form,
                                                             'all_tags': all_tags,
                                                             })
    return render(request, "search_categories.html", {"objects": objects, 'objects_count': objects_count,
                                                      'search_request': search_request,
                                                      'sellers': sellers, 'form': form, 'all_tags': all_tags,
                                                      'page': page_id})


def goods_modal(request, good_pk):
    """
    Shows goods as modal window in iframe
    :param request: HttpRequest
    :param good_pk: pk of good model
    :return: HttpResponse (rendered good_modal.html template)
    """
    good = get_object_or_404(Good, pk=good_pk)
    photos = GoodsPhotos.objects.filter(good=good)
    profile = good.get_user_profile()
    tags_ids = good.tags.values_list('id', flat=True)
    # photos_same_user = good.get_goods_photos_same_user()
    goods_with_tags = Good.objects.filter(tags__in=tags_ids).exclude(pk=good.pk).distinct()
    goods_with_max_likes = goods_with_tags.annotate(count=Count('users_like')).order_by('-count')[:9]
    goods_with_tags_right = goods_with_tags[:9]
    tags_ids = good.tags.values_list('id', flat=True)
    goods_comments = GoodsComments.objects.filter(good=good).order_by('-created')
    return render(request, 'good_modal.html', {'good':good, 'photos': photos, 'profile': profile,
                                               'goods_with_tags_right': goods_with_tags_right,
                                               'goods_with_max_likes': goods_with_max_likes, 'tag_ids': tags_ids,
                                               'goods_comments': goods_comments})


@ajax_required
@login_required
@require_POST
def add_to_wishlist(request):
    """
    Add/remove good to user wish list. Requires AJAX POST request
    :param request: HttpRequest (contains good id to add and action: add or remove)
    :return: JsonResponse
    """
    good_pk = request.POST['pk']
    action = request.POST['action']
    if good_pk and action:
        try:
            good = Good.objects.get(pk=good_pk)
            try:
                wishlist = WishList.objects.get(user=request.user)
            except WishList.DoesNotExist:
                wishlist = WishList(user=request.user)
                wishlist.save()
            if action == 'add':
                wishlist.goods.add(good)
            else:
                wishlist.goods.remove(good)
            return JsonResponse({'status': 'ok'})
        except Exception:
            pass
    return JsonResponse({'status': 'error'})


@ajax_required
@login_required
@require_POST
def add_user_like(request):
    """
    Add user to user_like goods field. Requires AJAX POST request
    :param request: HttpRequest (contains good id to add and action: add or remove)
    :return: JsonResponse
    """
    good_pk = request.POST['pk']
    action = request.POST['action']
    if good_pk and action:
        try:
            good = Good.objects.get(pk=good_pk)
            if action == 'add':
                good.users_like.add(request.user)
            else:
                good.users_like.remove(request.user)
            return JsonResponse({'status': 'ok'})
        except Exception:
            pass
    return JsonResponse({'status: error'})


@ajax_required
@require_POST
def goods_filter(request):
    """
    Count goods, that satisfy filter criteria. Requires AJAX POST request
    :param request: HttpRequest (contains filter criteria)
    :return: JsonResponse (count of goods)
    """
    all_goods = filtered_search(request.POST)
    goods_count = all_goods.count()
    return JsonResponse({'count': goods_count})


@ajax_required
@login_required
@require_POST
def add_new_tag(request):
    """
    Add new tag. Requires AJAX POST request
    :param request: HttpRequest (contains name of tag)
    :return: JsonResponse
    """
    tag_name = request.POST['tag_name']
    try:
        tag = Tag.objects.create(name=tag_name, slug=slugify(tag_name))
        return JsonResponse({'status': 'ok', 'id': tag.pk})
    except Exception:
        return JsonResponse({'status': 'error'})


def good_view(request, good_pk):
    """
    Shows good as page
    :param request: HttpRequest
    :param good_pk: pk of good model
    :return: HttpResponse (rendered good.html template)
    """
    # TODO: add integration with google translate
    good = get_object_or_404(Good, pk=good_pk)
    cleared_query = None
    if 'query_result' in request.session:
        # Convert stored string like ['1', '2'] to list and remove empty str values
        loaded_query_result = request.session['query_result'].strip('[').strip(']').split(',')
        cleared_query = [val for val in loaded_query_result if val != ""]
    if cleared_query:
        goods = Good.active.filter(pk__in=cleared_query).exclude(pk=good.pk).order_by('-created')
    else:
        goods = Good.active.all().exclude(pk=good.pk).order_by('-created')
    profile = good.get_user_profile()
    comments_count = good.comments.count()
    photos = GoodsPhotos.objects.filter(good=good)
    try:
        properties = good.properties
    except:
        properties = []
    tags_ids = good.tags.values_list('id', flat=True)
    goods_with_max_likes = goods.annotate(count=Count('users_like')).order_by('-count')[:8]
    random_goods_with_same_tags = goods.filter(tags__in=tags_ids).distinct().order_by('?')[:6]
    random_sellers_id = UserProfile.objects.filter(user__goods__tags__in=tags_ids).exclude(user=good.user).values_list('id', flat=True)
    random_sellers = UserProfile.objects.filter(pk__in=random_sellers_id).order_by('?')
    if len(random_sellers) > 0:
        random_goods_by_random_seller = Good.objects.filter(user__profile=random_sellers[0]).order_by('?')[:4]
        random_goods_slider = Good.objects.filter(user__profile=random_sellers[1]).order_by('?')[:2]
        random_seller = random_sellers[0]  # get first random seller in queryset
    else:
        random_goods_by_random_seller = None
        random_goods_slider = None
        random_seller = None
    paginator = Paginator(goods, ITEMS_COUNT)
    page = request.GET.get('page')
    try:
        goods = paginator.page(page)
    except PageNotAnInteger:
        goods = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        goods = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'good_ajax.html', {"goods": goods})
    return render(request, 'good.html', {'good': good, 'profile': profile, 'comments_count': comments_count,
                                         'photos': photos, 'properties': properties, 'random_seller': random_seller,
                                         'random_goods_by_random_seller' : random_goods_by_random_seller,
                                         'tags_ids': tags_ids, 'random_sellers': random_sellers[1:6], # get 5 random selleres in this category exept first
                                         'random_goods_with_same_tags': random_goods_with_same_tags, 'goods': goods,
                                         'goods_with_max_likes': goods_with_max_likes,
                                         'random_goods_slider': random_goods_slider})


@login_required
def add_good(request):
    """
    Add good view
    :param request: HttpRequest
    :return: HttpResponse (if error return rendered add_good.html else redirect to good page)
    """
    if request.method == 'POST':
        properties_form = GoodPropetiesForm(request.POST)
        good_form = GoodForm(request.POST)
        image_upload_form = CustomImageUpload(request.POST)
        if good_form.is_valid() and properties_form.is_valid() and image_upload_form.is_valid():
            # Get tags
            tags_names = good_form.cleaned_data['tags']
            tags = [Tag.objects.get(name=name) for name in tags_names]
            new_good = good_form.save(commit=False)
            new_good.user = request.user
            new_good.save()
            for tag in tags:
                new_good.tags.add(tag)
            new_good_properties = properties_form.save(commit=False)
            new_good_properties.good = new_good
            new_good_properties.save()
            # Get images ids
            images_ids = list(image_upload_form.cleaned_data.values())
            # Clear empty strings from images_ids
            indexes_images = len(images_ids) - 1
            while indexes_images >= 0:
                if not images_ids[indexes_images].isdigit():
                    images_ids.pop(indexes_images)
                indexes_images -= 1
            # Add photos only we have ids
            if len(images_ids) > 0:
                photos = GoodsPhotos.objects.filter(id__in=images_ids)
                photos.update(good=new_good)
            # Post to social networks with links
            site = get_current_site(request)
            post_to_social_network.delay(request.user.pk, new_good.pk, site.domain)
            return redirect(reverse('goods:good_view', args=[new_good.pk]))
        else:
            messages.error(request, _("Error adding goods"))
    else:
        image_upload_form = CustomImageUpload()
        good_form = GoodForm(initial={'deal': AUCTION})  # Set initial type to auction because it's first slider
        properties_form = GoodPropetiesForm()
    search_form = SearchForm()
    all_tags = Tag.objects.all()
    return render(request, 'add_good.html', {'search_form': search_form, 'good_form': good_form,
                                             'image_upload_form': image_upload_form,
                                             'properties_form': properties_form, 'all_tags': all_tags,
                                             })


@login_required
@ajax_required
@require_POST
def upload_good_photo(request):
    """
    Upload new image. Requires AJAX POST request
    :param request: HttpRequest (contains files with 'images' key)
    :return: JsonResponse
    """
    try:
        file = request.FILES['image']
        img = file
        photo = GoodsPhotos()
        photo.image = img
        photo.save()
        return JsonResponse({'photo': photo.pk, 'url': photo.image.url, 'status': 'ok'})
    except Exception:
        return JsonResponse({'status': 'error'})


@login_required
@ajax_required
@require_POST
def delete_photo(request):
    """
    Delete image. Requires AJAX POST request
    :param request: HttpRequest (contains pk key)
    :return: JsonResponse
    """
    pk = request.POST.get('pk', None)
    if pk:
        try:
            photo = GoodsPhotos.objects.get(pk=pk)
            photo.delete()
            return JsonResponse({'status': 'ok'})
        except (GoodsPhotos.DoesNotExist, GoodsPhotos.MultipleObjectsReturned):
            return JsonResponse({'status': 'error'})
    return JsonResponse({'status': 'error'})


@login_required
def show_wishlist(request):
    """
    Show user wishlist
    :param request: HttpRequest
    :return: HttpResponse
    """
    user = request.user
    try:
        wishlist = WishList.objects.get(user=user)
    except WishList.DoesNotExist:
        wishlist = WishList()
        wishlist.user = request.user
        wishlist.save()
    goods = wishlist.goods.all().select_related('user__profile')
    goods_count = goods.count()
    return render(request, 'wish_list.html',{'goods': goods, 'user': user, 'goods_count': goods_count})


@login_required
def edit_good(request, good_pk):
    """

    :param request:
    :param good_pk:
    :return:
    """
    # TODO: complete edit view
    search_form = SearchForm()
    image_upload_form = CustomImageUpload()
    good_form = GoodForm()
    properties_form = GoodPropetiesForm()
    all_tags = Tag.objects.all()
    return render(request, 'add_good.html', {'search_form': search_form, 'good_form': good_form,
                                             'image_upload_form': image_upload_form,
                                             'properties_form': properties_form, 'all_tags': all_tags})


class GoodDeleteView(DeleteView):
    """
    Delete good. Check if user is owner of good
    """
    model = Good
    success_url = reverse_lazy('cart:showcase_detail')
    template_name = 'delete_confirmation.html'

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        good = get_object_or_404(Good, pk=kwargs['pk'])
        if request.user == good.user:
            return super(GoodDeleteView, self).dispatch(request, *args, **kwargs)
        else:
            messages.error(self.request, _('You cannot delete this good'))
            return render(self.request, 'error.html')

    def get_context_data(self, **kwargs):
        context = super(GoodDeleteView, self).get_context_data(**kwargs)
        context['form'] = SearchForm()
        return context


@login_required
@ajax_required
@require_POST
def add_auction_bid(request):
    """
    Create user bid. Used by AJAX function makeBid.
    :param request: HttpRequest (contains 'id' and 'price' params)
    :return: JsonResponse
    """
    try:
        good = Good.active.get(id=request.POST.get('id'))
    except (Good.DoesNotExist, Good.MultipleObjectsReturned):
        return JsonResponse({'status': 'error', 'message': 'Product not found'})
    user_price = Decimal(request.POST.get('price'))
    if user_price > 0:
        max_bid = good.get_max_bid()
        if not max_bid:
            return JsonResponse({'status': 'error', 'message': 'Good is not on auction deal'})
        if user_price > Decimal(max_bid[0]):
            if not AuctionBids.objects.filter(accepted_by_seller=True).exists():
                user_bid = AuctionBids()
                user_bid.user = request.user
                user_bid.user_price = user_price
                user_bid.good = good
                user_bid.save()
                return JsonResponse({'status': 'ok'})
            else:
                return JsonResponse({'status': 'ok'})
        return JsonResponse({'status': 'error', 'message': 'Low bid'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Negative or zero price'})


@login_required()
@ajax_required
@require_POST
def reject_auction_bid(request):
    """
    Remove good from cart and remove all user bids for this good. Used by AJAX methods rejectBid()
    :param request: HttpRequest ( contain 'id' param)
    :return: JsonResponse
    """
    cart = Cart(request)
    try:
        good = Good.active.get(id=request.POST.get('id'))
    except Good.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'})
    bids = AuctionBids.objects.filter(good=good, user=request.user)
    if bids.exists():
        bids.delete()
    cart.remove(good)
    return JsonResponse({'status': 'ok'})


@login_required
@ajax_required
@require_POST
def set_inactive_good(request):
    """
    Set good to inactive, if it hasn't any bids.
    :param request: HttpRequest (AJAX from disableGood, contains good 'id')
    :return: JsonResponse
    """
    try:
        good = Good.active.get(id=request.POST.get('id'), user=request.user)
    except Good.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'})
    if good.bids.exists():
        return JsonResponse({'status': 'error', 'message': 'Good have a bids'})
    good.is_active = False
    good.save()
    AuctionCartModel.objects.filter(good=good).delete()
    return JsonResponse({'status': 'ok'})


@login_required
@ajax_required
@require_POST
def accept_bid(request):
    """
    Accept user bid.
    :param request: HttpRequest (AJAX from sellGood, contains good 'id' and user 'id')
    :return: JsonResponse
    """
    try:
        good = Good.active.get(id=request.POST.get('id'), user=request.user)
    except Good.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': 'Product not found'})
    try:
        buyer = User.objects.get(id=request.POST.get('user_id'))
    except User.DoesNotExist:
        return JsonResponse({'status': 'error', 'message': "User doesn't exists"})
    AuctionCartModel.objects.filter(good=good).exclude(user=buyer).delete()
    buyer_bid = AuctionBids.objects.filter(user=buyer, good=good).latest('created')
    buyer_bid.accepted_by_seller = True
    buyer_bid.save()
    return JsonResponse({'status': 'ok'})
