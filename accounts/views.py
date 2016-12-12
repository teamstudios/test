from datetime import timedelta

from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from django.views.decorators.http import require_POST
from django.db.models import Count
from django.core.files.base import ContentFile
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from django.conf import settings

from taggit.models import Tag

from storesb.settings import EMAIL_HOST_USER

from common.decorators import ajax_required
from common.functions import convert_str_to_float

from main.forms import SearchForm
from goods.models import Good
from goods.constants import ITEMS_COUNT

from complaints.constants import COMPLAINT_NOT_DEFINED, OWNER_IMPERSONATE, FRAUD, SPAM, ADVERTISE

from .tasks import send_email_task, send_api_request_task

from .models import ActivationProfile, UserProfile, Subscribers, Reviews, CardData, SocialNetwork
from .forms import UserRegistrationForm, PasswordResetEmailForm, PasswordResetPhoneForm, PasswordResetConfirmPhoneForm
from .forms import ProfileEditForm, UserEditForm, SetNewPassword
from .functions import generate_object_field, generate_activation_token, activate_profile, convert_str_to_image
from .functions import filtered_user_search
from .constants import SYMBOLS, DIGITS, LEGAL_ENTITY, PRIVATE_PERSON, MALE, FEMALE, NOT_DEFINED


# Create your views here.
def registration_page(request):
    """
    Show registration page. And confirm UserRegistrationForm submit.
    :param request: HttpRequest object
    :return: Page with rendered UserRegistrationForm. HttpResponse.
    """
    email_form_text = None
    phone_form_text = None
    timer_active = False
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            tomorrow = timezone.now() + timedelta(1)
            if cd['email']:
                try:
                    User.objects.get(email=cd['email'])
                    messages.error(request, _('User with this email already exists'))
                    return render(request, 'error.html')
                except User.MultipleObjectsReturned:
                    messages.error(request, _('User with this email already exists'))
                    return render(request, 'error.html')
                except User.DoesNotExist:
                    pass
                new_user = User(email=cd['email'], is_active=False,
                                username=generate_object_field(DIGITS, 6, User, 'username'))
                new_user.save()
                activation = ActivationProfile(user=new_user, token=generate_activation_token(new_user.username),
                                               valid_through=tomorrow)
                activation.save()
                email_message = _(
                    """Hello! You was registered on site storesb.com. \n
                    Your username: {username} \n
                    You should activate your account by clicking this link:
                    <a href="http://{site}/accounts/activation/{token}">
                    http://{site}/accounts/activation/{token}
                    </a> \n
                    Thank you!""".format(username=new_user.username, site=get_current_site(request),
                                         token=activation.token))
                send_email_task.delay("Activate your account", email_message, EMAIL_HOST_USER, new_user.email)
                email_form_text = _("""On this E-mail has been sent a letter.
                Click the link contained in it to complete the registration.""")
            if cd['phone']:
                try:
                    UserProfile.objects.get(phone=cd['phone'])
                    messages.error(request, _('User with this phone already exists'))
                    return render(request, 'error.html')
                except UserProfile.MultipleObjectsReturned:
                    messages.error(request, _('User with this phone already exists'))
                    return render(request, 'error.html')
                except UserProfile.DoesNotExist:
                    pass
                new_user = User(email=cd['email'], is_active=False,
                                username=generate_object_field(DIGITS, 6, User, 'username'))
                new_user.save()
                profile_user = UserProfile(user=new_user, slug=new_user.username, phone=cd['phone'])
                profile_user.save()
                activation = ActivationProfile(user=new_user,
                                               sms_key=generate_object_field(DIGITS, 6, ActivationProfile, 'sms_key'),
                                               valid_through=tomorrow)
                activation.save()
                text = "Your username: {username}. Your activation code on site {site} is: {code}".format(
                    username=new_user.username, site=get_current_site(request), code=activation.sms_key)
                send_api_request_task.delay(cd['phone'], text)
                phone_form_text = _("Enter the verification code in the SMS to complete the registration. "
                                    "You can request code again after 45 seconds")
                timer_active = True
            if cd['confirm_code']:
                if activate_profile('sms_key', cd['confirm_code'], request):
                    return redirect(reverse('accounts:reset_password'))
    else:
        form = UserRegistrationForm()
    return render(request, "registration.html", {"form": form, 'email_form_text': email_form_text,
                                                 'phone_form_text': phone_form_text, 'timer_active': timer_active})


def activation_view(request, token):
    """
    Activate user account by email link.
    :param request: HttpRequest
    :param token: token (field of ActivationProfile)
    :return: HttpResponse
    """
    if activate_profile('token', token, request):
        return redirect(reverse('accounts:reset_password'))
    else:
        return render(request, 'error.html')


@login_required()
def reset_password(request):
    """
    Show reset password form.
    :param request: HttpRequest
    :return: HttpResponse
    """
    if request.user.has_usable_password():
        return redirect(reverse('accounts:profile'))
    if request.method == 'POST':
        form = SetNewPassword(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            request.user.set_password(cd['password1'])
            request.user.save()
            update_session_auth_hash(request, request.user)
            return redirect(reverse('accounts:profile'))
    else:
        form = SetNewPassword()
    return render(request, 'reset_password.html', {'form': form})


@login_required
def profile_view(request):
    """
    User can edit and change his profile settings and password!
    :param request: HttpRequest
    :return:: HttpResponse
    """
    try:
        profile = UserProfile.objects.get(user=request.user)
    except UserProfile.DoesNotExist:
        profile = UserProfile.objects.create(user=request.user, slug=request.user.username)
    if request.method == 'POST':
        if 'password' in request.POST:
            user_edit_form = UserEditForm(instance=request.user)
            profile_edit_form = ProfileEditForm(instance=profile)
            password_form = PasswordChangeForm(user=request.user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)
                messages.success(request, _("Your password was changed"))
        elif 'edit' in request.POST:
            user_edit_form = UserEditForm(instance=request.user, data=request.POST)
            profile_edit_form = ProfileEditForm(instance=request.user.profile, data=request.POST)
            password_form = PasswordChangeForm(user=request.user)
            if user_edit_form.is_valid() and profile_edit_form.is_valid():
                user_edit_form.save()
                profile_edit_form.save()
                messages.success(request, _("Your profile was updated successfully"))
        else:
            messages.error(request, _("Request error!"))
            return render(request, 'error.html')
    else:
        password_form = PasswordChangeForm(user=request.user)
        user_edit_form = UserEditForm(instance=request.user)
        profile_edit_form = ProfileEditForm(instance=profile)
    return render(request, 'account.html', {'password_form': password_form,
                                            'user_edit_form': user_edit_form,
                                            'profile_edit_form': profile_edit_form})


def restore_password(request):
    """
    Show forms to restore password(by email, by phone and confirm code)
    :param request: HttpRequest
    :return: HttpResponse (rendered restore.html)
    """
    form_email = PasswordResetEmailForm()
    form_phone = PasswordResetPhoneForm()
    form_confirm = PasswordResetConfirmPhoneForm()
    return render(request, 'restore.html', {'form_email': form_email, 'form_phone': form_phone,
                                            'form_confirm': form_confirm})


def restore_send_email(request):
    """
    Check if email form is valid, user with this email exists and send email to him with password reset link.
    if method Get - return error string,
    if email was sent - return rendered template,
    if error in form or user doesn't exist - show template with forms again.
    :param request: HttpRequest (accept POST method)
    :return: HttpResponse
    """
    if request.method == 'POST':
        form_email = PasswordResetEmailForm(request.POST)
        if form_email.is_valid():
            cd = form_email.cleaned_data
            user = None
            try:
                user = User.objects.get(email=cd['email'])
            except (User.DoesNotExist, User.MultipleObjectsReturned):
                messages.error(request, _("User with this email doesn't exists"))
            if user:
                tomorrow = timezone.now() + timedelta(1)
                activation = ActivationProfile(user=user, token=generate_activation_token(user.username),
                                               valid_through=tomorrow)
                activation.save()
                email_message = _(
                    """Someone asked for password reset for email {email} on site storesb.com.
                    Follow the link below: <a href="http://{site}{link}">http://{site}{link}</a>
                    Your username, in case you've forgotten: {username}
                    Thank you!""".format(email=user.email, site=get_current_site(request),
                                         link=reverse('accounts:password_reset_link',
                                                      kwargs={'token': activation.token}),
                                         username=user.username))
                send_email_task.delay("Request for password reset", email_message, EMAIL_HOST_USER, user.email)
                return render(request, 'reset_email_sent.html')
        form_phone = PasswordResetPhoneForm()
        form_confirm = PasswordResetConfirmPhoneForm()
        return render(request, 'restore.html',
                      {'form_email': form_email, 'form_phone': form_phone, 'form_confirm': form_confirm})
    else:
        return HttpResponse("Incorrect request")


def restore_send_sms(request):
    """
    Check if phone form is valid, userprofile with this phone exists and send sms to him with password reset code.
    if method Get - return error string,
    if sms was sent - return rendered template,
    if error in form or user doesn't exist - show template with forms again.
    :param request: HttpRequest (accept POST method)
    """
    if request.method == 'POST':
        form_phone = PasswordResetPhoneForm(request.POST)
        form_email = PasswordResetEmailForm()
        form_confirm = PasswordResetConfirmPhoneForm()
        if form_phone.is_valid():
            cd = form_phone.cleaned_data
            user = None
            try:
                profile = UserProfile.objects.get(phone=cd['phone'])
                user = profile.user
            except (UserProfile.DoesNotExist, UserProfile.MultipleObjectsReturned):
                messages.error(request, _("User with this phone doesn't exists"))
            if user:
                tomorrow = timezone.now() + timedelta(1)
                activation = ActivationProfile(user=user,
                                               sms_key=generate_object_field(DIGITS, 6, ActivationProfile, 'sms_key'),
                                               valid_through=tomorrow)
                activation.save()
                text = "Your password reset code on site {site} is: {code}".format(site=get_current_site(request),
                                                                                   code=activation.sms_key)
                send_api_request_task.delay(cd['phone'], text)
                messages.success(request, _("Reset code was sent to your phone"))
            return render(request, 'restore.html', {'form_email': form_email, 'form_phone': form_phone,
                                                    'form_confirm': form_confirm})
    else:
        return HttpResponse("Incorrect request")


def password_confirm_code(request):
    """
    Check if code form is valid, set's new password and redirect him to his profile page
    to set new password.
    if method Get - return error string,
    if error in form or code is invalid - show error page.
    :param request: HttpRequest (accept POST method)
    """
    if request.method == 'POST':
        form_confirm = PasswordResetConfirmPhoneForm(request.POST)
        if form_confirm.is_valid():
            cd = form_confirm.cleaned_data
            if activate_profile('sms_key', cd['confirm_code'], request):
                return redirect(reverse('accounts:reset_password'))
        return render(request, 'error.html')
    else:
        return HttpResponse("Incorrect request")


@ajax_required
@login_required
@require_POST
def add_subscriber(request):
    """
    Add user to subscriber list. Requires AJAX post request.
    :param request: HttpRequest (contains user id to follow and action: add or remove)
    :return: JsonResponse
    """
    to_user_pk = request.POST['pk']
    action = request.POST['action']
    if to_user_pk and action:
        try:
            to_user = User.objects.get(pk=to_user_pk)
            try:
                subscribe = Subscribers.objects.get(owner=request.user)
            except Subscribers.DoesNotExist:
                subscribe = Subscribers.objects.create(owner=request.user)
            if action == 'add':
                subscribe.users.add(to_user)
            else:
                subscribe.users.remove(to_user)
            return JsonResponse({'status': 'ok'})
        except Exception:
            pass
    return JsonResponse({'status': 'error'})


def user_page(request, user_slug):
    """
    Show user page
    :param request: HttpRequest
    :param user_slug: profile.slug
    :return: HttpResponse
    """
    profile = get_object_or_404(UserProfile, slug=user_slug)
    about_reviews = profile.user.reviews.order_by('-created').select_related('author')[:3]
    user_goods = Good.objects.filter(user=profile.user)
    searchform = SearchForm()
    five_count = profile.get_mark_count_about(5)
    four_count = profile.get_mark_count_about(4.5) + profile.get_mark_count_about(4)
    three_count = profile.get_mark_count_about(3.5) + profile.get_mark_count_about(3)
    two_count = profile.get_mark_count_about(2.5) + profile.get_mark_count_about(2)
    one_count = profile.get_mark_count_about(1.5) + profile.get_mark_count_about(1)
    average_mark = round(profile.get_about_average_mark(), 1)
    all_to_user_sold_orders = profile.user.my_sold_orders.all().values_list('buyer', flat=True)
    goods_with_max_likes = Good.active.annotate(count=Count('users_like')).order_by('-count')[:7]
    return render(request, 'user_page.html', {'searchform': searchform, 'profile': profile,
                                              'about_reviews': about_reviews, 'user_goods': user_goods,
                                              'goods_with_max_likes': goods_with_max_likes,
                                              'five_count': five_count, 'four_count': four_count,
                                              'three_count': three_count, 'two_count': two_count,
                                              'one_count': one_count, 'average_mark': average_mark,
                                              'all_to_user_sold_orders': all_to_user_sold_orders,
                                              'GOOGLE_GEOCODING_KEY': settings.GOOGLE_GEOCODING_KEY,
                                              'COMPLAINT_NOT_DEFINED': COMPLAINT_NOT_DEFINED,
                                              'OWNER_IMPERSONATE': OWNER_IMPERSONATE, 'FRAUD': FRAUD, 'SPAM': SPAM,
                                              'ADVERTISE': ADVERTISE})


@require_POST
@login_required
@ajax_required
def upload_image(request):
    """
    Add user profile avatar or cover. Requires AJAX post request.
    :param request: HttpRequest (contains 'cover' or 'avatar' as key and base64 encoded data as value).
    :return: JsonResponse
    """
    try:
        user_profile = request.user.profile
        uid = user_profile.id
        cover_name = str(uid) + 'cover.png'
        if 'cover' in request.POST:
            img_str = request.POST['cover']
            img_data = convert_str_to_image(img_str)
            user_profile.cover.save(cover_name, ContentFile(img_data), save=True)
            user_profile.save()
            url = user_profile.cover.url
        elif 'avatar' in request.POST:
            img_str = request.POST['avatar']
            img_data = convert_str_to_image(img_str)
            user_profile.avatar.save('avatar.png', ContentFile(img_data), save=True)
            user_profile.save()
            url = user_profile.avatar.url
        else:
            return JsonResponse({'status': 'error'})
        return JsonResponse({'pk': user_profile.pk, 'url': url, 'status': 'ok'})
    except Exception:
        return JsonResponse({'status': 'error'})


@require_POST
@login_required
@ajax_required
def add_review(request):
    """
    Add review. Requires AJAX post request. Check if author can't write review to youself.
    :param request: HttpRequest (contains 'user_id', 'mark' and  'text').
    :return: JsonResponse
    """
    try:
        about_user = User.objects.get(pk=request.POST['user_id'])
    except (UserProfile.DoesNotExist, UserProfile.MultipleObjectsReturned):
        return JsonResponse({'status': 'error'})
    if request.user != about_user:
        all_to_user_sold_orders = about_user.my_sold_orders.all().values_list('buyer', flat=True)
        if request.user.pk in all_to_user_sold_orders:
            new_review = Reviews()
            new_review.author = request.user
            new_review.about_user = about_user
            new_review.mark = convert_str_to_float(request.POST.get('mark'))
            new_review.text = request.POST.get('text')
            new_review.save()
            return JsonResponse({'id': new_review.pk, 'text': new_review.text, 'mark': new_review.mark,
                                 'about': new_review.about_user.username, 'author': new_review.author.username,
                                 'status': 'ok', 'logo_url': request.user.profile.avatar.url })
    return JsonResponse({'status': 'error'})


@login_required
def show_subscriptions(request):
    """
    Show goods of sellers, on which user is subscribed
    :param request: HttpRequest
    :return: HttpResponse
    """
    user = request.user
    try:
        subscription = Subscribers.objects.get(owner=user)
    except Subscribers.DoesNotExist:
        subscription = Subscribers()
        subscription.owner = user
        subscription.save()
    subscriptions = subscription.users.all().select_related('user__profile')
    goods = Good.active.filter(user__in=subscriptions).order_by('-created')
    goods_count = goods.count()
    return render(request, 'wish_list.html', {'goods': goods, 'user': user, 'goods_count': goods_count,
                                              'section': 'subscriptions'})


def user_search(request):
    """
    Show users search page and perform search.
    :param request: HttpRequest if contains query parameter - then perform filtered search. Else - show all users.
    :return: HttpResponse
    """
    search_form = SearchForm()
    if 'query' in request.GET:
        users = filtered_user_search(request.GET)
        # Set page id and url to work with pagination and store request results
        page_id = 'query'
        search_request = request.GET.urlencode()
    else:
        users = User.objects.filter(is_active=True, is_staff=False).select_related('profile')
        page_id = None
        search_request = None
    tags = Tag.objects.all()
    paginator = Paginator(users, ITEMS_COUNT)
    page = request.GET.get('page')
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        if request.is_ajax():
            return HttpResponse('')
        users = paginator.page(paginator.num_pages)
    if request.is_ajax():
        return render(request, 'user_search_ajax.html', {"users": users})
    return render(request, 'user_search.html', {'search_form': search_form , 'users': users,
                                                'LEGAL_ENTITY': LEGAL_ENTITY, 'PRIVATE_PERSON': PRIVATE_PERSON,
                                                'MALE': MALE, 'FEMALE': FEMALE, 'NOT_DEFINED': NOT_DEFINED,
                                                'tags': tags, 'page_id': page_id, 'search_request': search_request})





def cropit(request):
    return render(request, 'cropit.html', {})
@login_required
@ajax_required
@require_POST
def snap_card(request):
    """
    Add card to account. Not used in this version.
    :param request:
    :return:
    """
    raise NotImplementedError("Not implemented yet")
    number = request.POST.get('card', None)
    month = request.POST.get('month', None)
    year = request.POST.get('year', None)
    if number and month and year:
        card = CardData()
        card.user = request.user
        card.number = number
        card.valid_throgh_month = month
        card.valid_throgh_year = year
        card.save()
        return JsonResponse({'status': 'ok'})
    return JsonResponse({'status': 'error'})
