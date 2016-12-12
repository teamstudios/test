from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from taggit.models import Tag

from main.models import BaseModel
from main.countries_list import COUNTRIES
from goods.models import Good

from .constants import LIME, ORANGE, NOT_DEFINED, PRIVATE_PERSON, LEGAL_ENTITY, MALE, FEMALE, VK, FACEBOOK, PINTEREST
from .constants import TWITTER, ODNOKLASSNIKI

# Create your models here.


class SocialNetwork(BaseModel):
    """
    SocialNetwork model. Store access tokens and name of soc. networks.
    """
    NETWORKS = (
        (VK, "VK"),
        (FACEBOOK, "Facebook"),
        (PINTEREST, "Pinterest"),
        (TWITTER, "Twitter"),
        (ODNOKLASSNIKI, "Odnoklassniki")
    )
    title = models.CharField(max_length=100, verbose_name=_("Title"))
    network_id = models.CharField(choices=NETWORKS, verbose_name=_('Network ID'), unique=True, null=True, blank=True,
                                  max_length=20)

    def __str__(self):
        return self.title
#
#
# class SocialAccount(BaseModel):
#     """
#     User social accounts. Store link to user social network page and setting to post on his page.
#     """
#     user = models.OneToOneField(User, related_name="social_account")
#     social_network = models.ForeignKey(SocialNetwork, verbose_name=_("Social network"))
#     account_link = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("Account link"))
#     auto_post_updated = models.BooleanField(default=False, verbose_name=_("Auto post"))
#
#     def __str__(self):
#         return self.user.username


class UserProfile(BaseModel):
    """
    User profile.
    """
    ORG_FORM = (
        (PRIVATE_PERSON, _("Private person")),
        (LEGAL_ENTITY, _("Legal entity")),
        # (2, _("Individual entrepreneur"))
    )
    SEX = (
        (MALE, _('MALE')),
        (FEMALE, _('FEMALE')),
        (NOT_DEFINED, _('NOT DEFINED'))
    )
    USER_THEME = (
        (LIME, _("LIME")),
        (ORANGE, _("ORANGE")),
        (NOT_DEFINED, _("NOT DEFINED"))
    )
    STATUS = (
        (0, _("Offline")),
        (1, _("Online"))
    )

    user = models.OneToOneField(User, related_name="profile")
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, verbose_name=_("Avatar"))
    cover = models.ImageField(upload_to='covers', blank=True, null=True, verbose_name=_("Cover"))
    description = models.TextField(null=True, blank=True, verbose_name=_("About"))
    sex = models.IntegerField(choices=SEX, default=2, verbose_name=_("SEX"))
    org_form = models.IntegerField(choices=ORG_FORM, default=0, verbose_name=_("Form of incorporation"))
    country = models.CharField(max_length=3, verbose_name=_("Country"), choices=COUNTRIES, default='RU')
    city = models.CharField(max_length=255, null=True, blank=True, verbose_name=_("City"))
    phone = models.CharField(verbose_name=_("Phone"), null=True, blank=True, max_length=20)
    additional_phone = models.CharField(verbose_name=_("Additional phone"), null=True, blank=True, max_length=20)
    skype = models.CharField(max_length=255, null=True, blank=True, verbose_name="Skype")
    instagram = models.CharField(max_length=255, null=True, blank=True, verbose_name="Instagram")
    site = models.CharField(verbose_name="Web site", null=True, blank=True, max_length=128)
    map_link = models.TextField(verbose_name=_("Google map link"), null=True, blank=True)
    slug = models.SlugField(max_length=255, verbose_name=_("Profile link"), unique=True)
    theme = models.IntegerField(choices=USER_THEME, default=2, verbose_name=_("Theme"))
    status = models.IntegerField(choices=STATUS, default=1, verbose_name=_("User online status"))
    auto_post_to_networks = models.ManyToManyField(SocialNetwork, verbose_name=_('Allow auto post to'))

    def avatar_tag(self):
        return u'<img src="%s" height=75 width=75 />' % (self.avatar.url)

    avatar_tag.short_description = _("Current avatar")
    avatar_tag.allow_tags = True

    def __str__(self):
        return self.user.username

    def get_all_about_marks(self):
        marks = Reviews.objects.filter(about_user=self.user).values_list('mark', flat=True)
        return marks

    def get_my_marks(self):
        marks = Reviews.objects.filter(author=self.user).values_list('mark', flat=True)
        return marks

    def get_absolute_url(self):
        return reverse('user_page', args=[self.slug])

    def get_mark_count_about(self, mark):
        marks_count = Reviews.objects.filter(about_user=self.user).filter(mark=mark).count()
        return marks_count

    def get_about_average_mark(self):
        marks = self.get_all_about_marks()
        avg = 0
        sum = 0
        if len(marks) > 0:
            for mark in marks:
                sum += mark
            avg = sum / len(marks)
        return avg

    def get_total_about_marks(self):
        marks_count = Reviews.objects.filter(about_user=self.user).count()
        return marks_count

    def get_lots_count(self):
        lots_count = self.user.goods.count()
        return lots_count

    def get_subscribers_count(self):
        count_lists = Subscribers.objects.filter(users=self.user).count()
        return count_lists

    def get_subscription_count(self):
        my_list = Subscribers.objects.get(owner=self.user)
        count = my_list.users.count()
        return count

    def get_user_tags(self):
        """
        Get all user tags
        :return:
        """
        goods = Good.objects.filter(user=self.user)
        tags = Tag.objects.filter(good__in=goods).distinct()
        return tags

    class Meta:
        ordering = ('updated',)


class ActivationProfile(models.Model):
    """
    Model to store email token or sms code for registration.
    """
    user = models.ForeignKey(User)
    token = models.CharField(max_length=255)
    sms_key = models.CharField(max_length=10)
    valid_through = models.DateTimeField()
    password_reset = models.BooleanField(default=False)


class UserComments(BaseModel):
    """

    """
    about_user = models.ForeignKey(User, related_name='about_comments')
    user = models.ForeignKey(User, related_name='users_comments')
    text = models.TextField(verbose_name=_('Comment'))

    def __str__(self):
        return self.about_user.title

    class Meta:
        ordering = ('created',)


class Subscribers(BaseModel):
    """

    """
    owner = models.OneToOneField(User, related_name='subscribers')
    users = models.ManyToManyField(User, related_name='subscriptions')

    def __str__(self):
        return self.owner.username

    class Meta:
        ordering = ('created',)


class Reviews(BaseModel):
    """

    """
    MARKS = (
        (0, 0),
        (0.5, 0.5),
        (1, 1),
        (1.5, 1.5),
        (2, 2),
        (2.5, 2.5),
        (3, 3),
        (3.5, 3.5),
        (4, 4),
        (4.5, 4.5),
        (5, 5)
    )
    about_user = models.ForeignKey(User, related_name='reviews')
    author = models.ForeignKey(User, related_name='my_reviews')
    text = models.TextField(verbose_name=_('Text'))
    mark = models.DecimalField(choices=MARKS, default=0, max_digits=3, decimal_places=1)

    def __str__(self):
        return self.about_user.username + ' ' + str(self.mark)

    class Meta:
        ordering = ('created',)


class CardData(BaseModel):
    user = models.ForeignKey(User, related_name='cards', verbose_name=_('User'))
    number = models.BigIntegerField(verbose_name=_('Card number'))
    valid_throgh_month = models.IntegerField(verbose_name=_('Month'))
    valid_throgh_year = models.IntegerField(verbose_name=_('Year'))

    def __str__(self):
        return self.user.username + ' ' + 'card'

    class Meta:
        ordering = ('updated', )
