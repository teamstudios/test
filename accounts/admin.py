from django.contrib import admin
from .models import UserProfile, ActivationProfile, UserComments, Subscribers, Reviews
from .models import CardData, SocialNetwork # , SocialAccount,

# Register your models here.


class SocialNetworkAdmin(admin.ModelAdmin):
    list_display = ("title", "network_id","updated")
    list_filter = ("created", "updated")
    ordering = ["title", "created"]


# class SocialAccountsAdmin(admin.ModelAdmin):
#     list_display = ("user", "social_network", "auto_post_updated")
#     list_filter = ("social_network", "auto_post_updated", "updated", "created")
#     search_fields = ('user',)
#     ordering = ["updated"]


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'slug', 'org_form', 'created', 'updated')
    list_filter = ('sex', 'city', 'country',)
    search_fields = ('user__username', 'description', 'country', 'city', 'phone', 'skype')
    date_hierarchy = 'updated'
    ordering = ['updated', "user"]
    readonly_fields = ('avatar_tag',)


class ActivationProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'valid_through')


class UserCommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'about_user', 'created')
    list_filter = ('user', 'about_user')
    search_fields = ('text',)


class SubscribersAdmin(admin.ModelAdmin):
    list_display = ('owner', 'updated')
    search_fields = ('owner__username',)


class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('author', 'about_user', 'mark', 'created')
    list_filter = ('mark', 'created',)
    search_fields = ('text', 'author__username')


class CardDataAdmin(admin.ModelAdmin):
    list_display = ('user', 'number')


admin.site.register(SocialNetwork, SocialNetworkAdmin)
# admin.site.register(SocialAccount, SocialAccountsAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(ActivationProfile, ActivationProfileAdmin)
admin.site.register(UserComments, UserCommentsAdmin)
admin.site.register(Subscribers, SubscribersAdmin)
admin.site.register(Reviews, ReviewsAdmin)
admin.site.register(CardData, CardDataAdmin)