"""storesb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf.urls.static import static

from filebrowser.sites import site

from storesb.settings import MEDIA_ROOT, MEDIA_URL

from main.views import index_view
from accounts.views import user_page, cropit


urlpatterns = [
    url(r'^$', index_view, name='index'),
    url(r'^main/', include('main.urls', namespace='main', app_name='main')),
    url(r'^goods/', include('goods.urls', namespace='goods', app_name='goods')),
    url(r'^accounts/', include('accounts.urls', namespace='accounts', app_name='accounts')),
    url(r'^complaints/', include('complaints.urls', namespace='complaints', app_name='complaints')),
    url(r'^chat/', include('chat.urls', namespace='chat', app_name='chat')),
    url(r'^cart/', include('cart.urls', namespace='cart', app_name='cart')),
    url('^pages/', include('pages.urls', namespace='pages', app_name='pages')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/', admin.site.urls),
    url(r'^tinymce/', include('tinymce.urls')),
    url(r'social-auth/', include('social.apps.django_app.urls', namespace='social')),
    url(r'^i18n/', include('django.conf.urls.i18n')),
    url(r'^(?P<user_slug>\w+)/$', user_page, name='user_page'),
    url(r'^cropit$', cropit, name='cropit'),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
