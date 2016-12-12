import logging
import facebook
import vk

from django.utils import timezone
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.staticfiles.templatetags.staticfiles import static
from django.conf import settings

from celery.task import task

from cart.models import AuctionCartModel
from accounts.constants import FACEBOOK, PINTEREST, VK
from common.pinterest import Pinterest

from .models import Good
from .constants import AUCTION

log = logging.getLogger(__name__)


@task
def set_disabled_goods():
    """
    Run every minute to disable goods if their valid_through date is less then now
    """
    log.debug("Tasks set_disabled_goods running")
    now = timezone.now()
    goods = Good.active.filter(deal=AUCTION, valid_through__lte=now)
    if goods.exists():
        AuctionCartModel.objects.filter(good__in=goods).delete()
        goods.update(is_active=False)
        log.debug("Goods updated")


@task(name="post-to-social-network")
def post_to_social_network(user_id, good_id, site):
    """
    Try to post to social networks. Get allowed networks to post from user profile
    :param user_id: user.pk to from want to post
    :param good_id: added good
    :param site: current site
    :return: nothing
    """
    try:
        user = User.objects.get(pk=user_id)
        good = Good.objects.get(pk=good_id)
    except ObjectDoesNotExist:
        log.error("User: {user_id} or good: {good_id} with this id doesn't exist".format(user_id=user_id,
                                                                                         good_id=good_id))
        return
    network_list = user.profile.auto_post_to_networks.all()
    message = "Selling new good {g_name}! You can buy it at http://{site}{link}".format(site=site, g_name=good.title,
                                                                           link=good.get_absolute_url())
    for network in network_list:
        # Get allowed network list. If user haven't added account do nothing (just log)
        try:
            social = user.social_auth.get(provider=network.network_id)
            token = social.extra_data["access_token"]
        except (ObjectDoesNotExist, KeyError):
            log.error("User {user} haven't social account to {network}".format(user=user.username,
                                                                               network=network.network_id))
            continue
        # Post to facebook
        if network.network_id == FACEBOOK:
            log.debug("Try to posting facebook")
            try:
                fb_api = facebook.GraphAPI(access_token=token)
                response = fb_api.post('me/feed', params={"message": message})
                log.debug("Response posting: {}".format(response))
            except Exception as e:
                log.error("Exception: {}".format(e))
        if network.network_id == VK:
            pass
            # TODO: Commented. Reason: Access denied: no access to call this method. Sites not allowed to post on VK wall
            # log.debug("Try to posting vk")
            # try:
            #     session = vk.Session(access_token=token)
            #     vk_api = vk.API(session)
            #     response = vk_api.users.get()
            #     id = response[0].get('uid', None)
            #     if id:
            #         owner_id = "-" + str(id)
            #         response = vk_api.wall.post(message=message, owner_id=owner_id)
            #         log.debug("Response posting: {}".format(response))
            #     else:
            #         log.debug("User id not found")
            # except Exception as e:
            #     log.error("Exception: {}".format(e))
        if network.network_id == PINTEREST:
            # post godd as pint to pinterest
            if good.get_first_image():
                image = good.get_first_image()
                image_url = "http://{site}{link}".format(site=site, link=image.image.url)
            else:
                image = static(settings.NO_GOOD)
                image_url = "http://{site}{link}".format(site=site, link=image)
            pinterest = Pinterest(token, user)
            pinterest.post_message(message, image_url)
