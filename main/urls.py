from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^calculator/$', views.calculator_view, name='calculator'),
]