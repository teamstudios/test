from django.contrib import admin

from .models import Thread, Message

# Register your models here.


class ThreadAdmin(admin.ModelAdmin):
    list_display = ('pk', "last_message", )
    list_filter = ("last_message", )


class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'thread', 'datetime')
    list_filter = ('sender', 'thread', 'datetime')
    search_fields = ('text', 'sender__username')
    date_hierarchy = 'datetime'
    ordering = ['datetime']


admin.site.register(Thread, ThreadAdmin)
admin.site.register(Message, MessageAdmin)
