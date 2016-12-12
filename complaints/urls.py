from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add-complaint/$', views.add_complaint, name='add_complaint'),
    url(r'^remove-from-blocklist', views.remove_from_block, name='remove_from_block'),
]