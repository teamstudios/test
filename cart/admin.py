from django.contrib import admin

from .models import AuctionCartModel

# Register your models here.


class AuctionCartAdmin(admin.ModelAdmin):
    list_display = ('user', 'good', 'created', 'updated')
    date_hierarchy = 'created'
    ordering = ['created', "user"]


admin.site.register(AuctionCartModel, AuctionCartAdmin)
