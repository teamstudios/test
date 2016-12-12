import hashlib
import random
import base64

from django.contrib import messages
from django.utils import timezone
from django.utils.translation import ugettext as _
from django.contrib.auth import login, authenticate
from django.contrib.auth.models import User
from django.db.models import Q

# from .authentication import TokenAuthBackend

from goods.models import Good

from main.countries_list import COUNTRIES
from common.functions import convert_str_to_int

from .models import ActivationProfile, UserProfile
from .constants import SYMBOLS, NOT_DEFINED, LIME, ORANGE


def generate_random_string(symbols, length):
    """
    Generate string from symbols.
    :param symbols: String of symbols divided by space.
    :param length: Length of generated string
    :return: String
    """
    sym_list = symbols.split()
    str_list = random.sample(sym_list, length)
    gen_string = ''.join(str_list)
    return gen_string


def generate_object_field(symbols, length, object, field):
    """
    Generate unique value of field of object
    :param symbols: String of symbols divided by space.
    :param length: Length of generated string
    :param object: Object to check for generated field value
    :param field: Field which should be unique
    :return: String
    """
    string = generate_random_string(symbols, length)
    try:
        instance = object.objects.get(**{field:string})
        if instance:
            string = generate_object_field(symbols, length, object, field)
    except object.DoesNotExist:
        pass
    return string


def generate_activation_token(username):
    """
    Generate activation token as sha1 hash of random number + sha1 hash of username
    :param username: Username as string
    :return: string
    """
    salt = hashlib.sha1(str(random.random()).encode('utf-8')).hexdigest()[:5]
    encoded_string = salt + username
    token = hashlib.sha1(encoded_string.encode('utf-8')).hexdigest()
    try:
        profile = ActivationProfile.objects.get(token=token)
        if profile:
            token = generate_activation_token(username)
    except ActivationProfile.DoesNotExist:
        pass
    return token


def activate_profile(field, code, request):
    """
    Find activation profile by field (token or sms) and code. Activate user object, set password,
    and delete activation profile. Also authenticate user.
    :param field: field name  for lookup
    :param code: code for lookup by field
    :param request: HttpRequest object
    :param password_reset: True if password reset, False if first activation
    :return: Boolean, true if success, false if exception.
    """
    try:
        activation = ActivationProfile.objects.get(**{field:code})
    except ActivationProfile.DoesNotExist:
        messages.error(request, _('Activation code expired or not valid!'))
        return False
    if timezone.now() < activation.valid_through:
        activation.user.is_active = True
        activation.user.set_unusable_password()
        activation.user.save()
        if request.user.is_anonymous():
            if field == 'token':
                user = authenticate(username=activation.user.username, token=activation.token)
            elif field == 'sms_key':
                user = authenticate(username=activation.user.username, code=activation.sms_key)
            else:
                user = None
            activation.delete()
            if user:
                login(request, user)
                messages.success(request, _("""Profile activated successfully! You should change your password!"""))
                return True
            else:
                return False


def define_theme(request):
    """

    :param request:
    :return:
    """
    if request.user.is_anonymous():
        theme_id = NOT_DEFINED
    else:
        try:
            theme_id = request.user.profile.theme
        except UserProfile.DoesNotExist:
            theme_id = NOT_DEFINED
    if theme_id == NOT_DEFINED:
        theme_id = random.choice([LIME, ORANGE])
    return theme_id


def convert_str_to_image(image_string):
    """
    Convert base 64 string withe headers to image
    :param image_string: str (encoded base64)
    :return: img_data
    """
    image = image_string.partition('base64,')[2]
    img_data = base64.b64decode(image)
    return img_data


def filtered_user_search(request_method):
    """
    Perform the filter by criteria
    :param request_method: request.GET or request.POST
    :return: Users queryset
    """
    all_users = User.objects.filter(is_active=True, is_staff=False).select_related('profile')
    if 'name' in request_method:
        all_users = all_users.filter(username__icontains=request_method['name'])
    if 'location' in request_method:
        country = None
        for cntr in COUNTRIES:
            if request_method['location'].casefold() in cntr[1].casefold():
                country = cntr[0]
        all_users = all_users.filter(Q(profile__city__icontains=request_method['location']) | Q(profile__country=country))
    if 'orgform' in request_method:
        if convert_str_to_int(request_method['orgform']) != NOT_DEFINED:
            all_users = all_users.filter(profile__org_form=request_method['orgform'])
    if 'status' in request_method:
        if convert_str_to_int(request_method['status']) != NOT_DEFINED:
            all_users = all_users.filter(profile__status=request_method['status'])
    if 'sex' in request_method:
        if convert_str_to_int(request_method['sex']) != NOT_DEFINED:
            all_users = all_users.filter(profile__sex=request_method['sex'])
    if 'cooperation' in request_method:
        goods = Good.objects.filter(cooperation__icontains=request_method['cooperation'])
        all_users = all_users.filter(goods__in=goods).distinct()
    if 'tag_id[]' in request_method:
        tags_ids = request_method.getlist('tag_id[]')
        goods = Good.objects.filter(tags__in=tags_ids).distinct()
        all_users = all_users.filter(goods__in=goods).distinct()
    return all_users