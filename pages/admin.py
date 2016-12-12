from django.contrib import admin

from parler.admin import TranslatableAdmin

from .models import Page

# Register your models here.


class PageAdmin(TranslatableAdmin):
    list_display = ('title', 'url', 'created', 'updated')
    list_filter = ('created', )
    search_fields = ('title', 'content', 'ceo_keywords', 'ceo_description')
    date_hierarchy = 'created'
    ordering = ['created']

    def get_prepopulated_fields(self, request, obj=None):
        return {'url': ('title',)}


admin.site.register(Page, PageAdmin)
