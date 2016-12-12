from django.contrib import admin
from .models import Complaint, BlockList

# Register your models here.


class ComplaintAdmin(admin.ModelAdmin):
    list_display = ['complaint_from', 'complaint_to', 'complaint_type', 'created']
    list_filter = ['complaint_type', 'created']
    search_fields = ['text']


admin.site.register(Complaint, ComplaintAdmin)
admin.site.register(BlockList)
