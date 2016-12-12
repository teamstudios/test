from django.db import models
from django.db.models import Max
from django.core.exceptions import FieldError
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist

from taggit.managers import TaggableManager

from main.models import BaseModel
from .constants import MAX_PHOTOS_COUNT, BUY_SELL, SALE, AUCTION, LOGISTIC, MAIL, COURIER, HANDS, PICKUP, NEW, USED
from .constants import MONETARY, REPLACEMENT, TO_BUYER, BY_SELLER

# Create your models here.


class ActiveManager(models.Manager):
    """
    Active manager to get all active goods
    """
    def get_queryset(self):
        return super(ActiveManager, self).get_queryset().filter(is_active=True)


class Good(BaseModel):
    """
    Goods model.
    """
    STATE = (
        (NEW, _("New")),
        (USED, _("Used"))
    )
    DEAL = (
        (BUY_SELL, _("Buy-Sell")),
        (SALE, _("Sale")),
        (AUCTION, _("Auction"))
    )
    DELIVERY_FORMS = (
        (LOGISTIC, _("Logistic")),
        (MAIL, _("Mail")),
        (COURIER, _("Courier")),
        (HANDS, _("Hands")),
        (PICKUP, _("Pickup"))
    )
    BACK_DELIVERY_FORMS = (
        (TO_BUYER, _("Due to buyer")),
        (BY_SELLER, _("By seller"))
    )
    REFUND = (
        (MONETARY, _("Monetary equivalent")),
        (REPLACEMENT, _("Replacement product"))
    )
    title = models.CharField(max_length=255, verbose_name=_('Title'))
    quantity = models.IntegerField(default=1, verbose_name=_('Quantity'))
    old_price = models.DecimalField(default=0.0, verbose_name=_('Old price (Sale)'), max_digits=10, decimal_places=2)
    new_price = models.DecimalField(default=0.0, verbose_name=_('New price (Sale)'), max_digits=10, decimal_places=2)
    price = models.DecimalField(default=0.0, verbose_name=_('Price (Buy-Sell)'), max_digits=10, decimal_places=2)
    min_price = models.DecimalField(default=0.0, verbose_name=_('Min price (Auction)'), max_digits=10, decimal_places=2)
    reserve_price = models.DecimalField(default=0.0, verbose_name=_('Reserve price (Auction)'), max_digits=10,
                                        decimal_places=2)
    max_price = models.DecimalField(default=0.0, verbose_name=_('Max price (Auction)'), max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, related_name='goods')
    state = models.IntegerField(choices=STATE, default=0, verbose_name=_('State'))
    delivery_form = models.IntegerField(choices=DELIVERY_FORMS, default=MAIL, verbose_name=_("Delivery form"))
    delivery_time = models.CharField(default=str(1), verbose_name=_("Delivery time"), null=True, blank=True, max_length=128)
    cooperation = models.CharField(max_length=255, verbose_name=_("Cooperation"), default=_("All countries"))
    deal = models.IntegerField(choices=DEAL, default=0, verbose_name=_('Type of deal'))
    refund = models.IntegerField(choices=REFUND, default=0, verbose_name=_('Refund'))
    purchase_returns_time = models.CharField(default=str(1), verbose_name=_("Purchase returns time"), max_length=128)
    back_delivery_form = models.IntegerField(choices=BACK_DELIVERY_FORMS, default=0, verbose_name=_("Back delivery form"))
    tags = TaggableManager()
    delivery_description = models.TextField(null=True, blank=True, verbose_name=_("Delivery description"))
    location = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Location"))
    users_like = models.ManyToManyField(User, related_name='goods_liked', blank=True)
    valid_through = models.DateTimeField(null=True, blank=True, verbose_name=_("Valid through"))
    is_active = models.BooleanField(default=True, verbose_name=_("Active"))
    objects = models.Manager()
    active = ActiveManager()

    def __str__(self):
        return self.title

    def get_photos_counts(self):
        """
        Return count of good photos
        :return: int
        """
        return GoodsPhotos.objects.filter(good=self).count()

    def get_first_image(self):
        """
        Get first photo of good. And if exist - return it. Else return None.
        :return: GoodsPhoto object or None
        """
        photos = GoodsPhotos.objects.filter(good=self)[:1]
        if photos:
            return photos[0]
        else:
            return None

    def get_sale_percent(self):
        """
        Calculate sale percent
        :return: int
        """
        if self.deal == SALE:
            diff = self.old_price - self.new_price
            percent = diff / (self.old_price / 100)
            return round(percent, 0)

    def get_good_price_by_deal(self):
        """

        :return:
        """
        if self.deal == SALE:
            return self.new_price
        elif self.deal == AUCTION:
            return self.max_price
        else:
            return self.price

    def get_user_profile(self):
        """
        Get profile of user, whom created this good
        :return: UserProfile object
        """
        return self.user.profile

    def get_goods_photos_same_user(self):
        """
        Get photos of same user
        :return: GoodsPhotos queryset
        """
        photos = GoodsPhotos.objects.filter(good__user=self.user).exclude(good=self)
        return photos

    def get_max_bid(self):
        """
        Get max bids on this good, and return max_price and username
        :return: tuple(Decimal, str)
        """
        if self.deal == AUCTION:
            max_bid = self.bids.aggregate(Max('user_price'))
            if max_bid['user_price__max'] is not None:
                user = self.bids.get(user_price=max_bid['user_price__max']).user
                return max_bid['user_price__max'], user.username
            else:
                return 0, None
        else:
            return False

    def get_last_bid(self, username):
        """
        Return user bid for this good
        :param username: username (str)
        :return: Decimal or None
        """
        try:
            good_bid = AuctionBids.objects.filter(good=self, user__username=username).latest('created')
            return good_bid.user_price
        except ObjectDoesNotExist:
            return None

    def check_accepted_bid(self, username):
        """
        Check if user's bid are accepted by selller
        :param username: str Username
        :return: Bool
        """
        good_bids = AuctionBids.objects.filter(good=self, user__username=username, accepted_by_seller=True)
        if good_bids.exists():
            return True
        return False

    def has_accepted_bids(self):
        """
        Check if good has accepted bids
        :return: Bool
        """
        good_bids = AuctionBids.objects.filter(good=self, accepted_by_seller=True)
        if good_bids.exists():
            return True
        return False

    def get_absolute_url(self):
        return reverse('goods:good_view', args=[self.pk])

    class Meta:
        ordering = ('created',)


class GoodsProperties(BaseModel):
    """
    Goods properties model
    """
    good = models.OneToOneField(Good, related_name='properties')
    description = models.TextField(null=True, blank=True, verbose_name=_("Description"))
    trade_mark = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Trade mark"))
    material = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Material"))
    color = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Color"))
    equipment = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Equipment"))
    model = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Model"))
    size = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Size"))
    weight = models.DecimalField(null=True, blank=True, verbose_name=_("Weight (kg.)"), max_digits=10, decimal_places=2)
    vendor = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Vendor"))

    def __str__(self):
        return self.good.title


class TranslatedText(BaseModel):
    """
    Model for store translated goods description
    """
    language_code = models.CharField(max_length=12, verbose_name=_("Language code"))
    translated_text = models.TextField(verbose_name=_('Translated text'))
    good_properties = models.ForeignKey(GoodsProperties)

    def __str__(self):
        return self.good_properties.good.title


class GoodsPhotos(BaseModel):
    """
    Model to store goods photos
    """
    good = models.ForeignKey(Good, related_name='goods_photos', null=True, blank=True)
    image = models.ImageField(upload_to='goods', verbose_name=_('Image'))

    def __str__(self):
        if self.good:
            return self.good.title
        else:
            return "No goods defined"

    def save(self, *args, **kwargs):
        if self.good and self.good.get_photos_counts() >= MAX_PHOTOS_COUNT:
            raise FieldError("Photos count more then {}".format(MAX_PHOTOS_COUNT))
        else:
            super(GoodsPhotos, self).save(*args, **kwargs)

    class Meta:
        ordering = ('created',)


class GoodsComments(BaseModel):
    """
    Model to store comments about good
    """
    good = models.ForeignKey(Good, related_name='comments')
    user = models.ForeignKey(User, related_name='goods_comments')
    text = models.TextField(verbose_name=_('Comment'))

    def __str__(self):
        return self.good.title

    class Meta:
        ordering = ('created',)


class AuctionBids(BaseModel):
    """
    Store user's bids, for product with deal == AUCTION
    """
    good = models.ForeignKey(Good, related_name='bids')
    user = models.ForeignKey(User, related_name='user_bids')
    user_price = models.DecimalField(default=0.0, verbose_name=_('User price'), max_digits=10, decimal_places=2)
    accepted_by_seller = models.BooleanField(default=False, verbose_name=_('Bid accepted'))

    def __str__(self):
        return self.good.title + ":" + self.user.username

    class Meta:
        ordering = ('created',)


class WishList(BaseModel):
    """
    Stores users goods, which he want to buy
    """
    user = models.OneToOneField(User, related_name='wishlist')
    goods = models.ManyToManyField(Good, related_name='wishlists')

    def __str__(self):
        return self.user.username

    class Meta:
        ordering = ('created',)
