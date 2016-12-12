from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^page/(?P<url>[-\w]+)/$', views.PageDetailView.as_view(), name='page_view'),
]