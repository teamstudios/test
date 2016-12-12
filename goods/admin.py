from django.contrib import admin
from .models import Good, GoodsProperties, GoodsPhotos, GoodsComments
# This import may be deleted or changed
from .models import TranslatedText, AuctionBids, WishList

# Register your models here.


class GoodAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'created', 'deal', 'is_active', 'valid_through')
    list_filter = ('deal', 'created', 'is_active')
    search_fields = ('title', 'delivery_description')
    date_hierarchy = 'created'
    ordering = ['created']


class GoodsPropertiesAdmin(admin.ModelAdmin):
    list_display = ('good', 'created')
    list_filter = ('created',)
    search_fields = ('good__title', 'description')


class GoodsPhotosAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created',)
    list_filter = ('created', )


class GoodsCommentsAdmin(admin.ModelAdmin):
    list_display = ('user', 'good', 'created')
    list_filter = ('user', 'good')
    search_fields = ('text',)


class WishListAdmin(admin.ModelAdmin):
    list_display = ('user', 'updated')
    search_fields = ('user__username',)


class AuctionBidsAdmin(admin.ModelAdmin):
    list_display = ('good', 'user', 'user_price', 'created')


admin.site.register(Good, GoodAdmin)
admin.site.register(GoodsProperties, GoodsPropertiesAdmin)
admin.site.register(GoodsPhotos, GoodsPhotosAdmin)
admin.site.register(GoodsComments, GoodsCommentsAdmin)
admin.site.register(AuctionBids, AuctionBidsAdmin)
admin.site.register(WishList, WishListAdmin)
# This may be deleted
admin.site.register(TranslatedText)