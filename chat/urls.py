from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^thread-list/$', views.show_threads_list, name='show_thread_list'),
    url(r'^send-message/$', views.send_message, name='send_message'),
    url(r'^thread/(?P<thread_id>\d+)/$', views.show_thread, name='show_thread'),
    url(r'^send_message_api/$', views.send_message_api, name='send_message_api'),
    url(r'^check_username/$', views.check_username, name='check_username'),
    url(r'^send_message_ajax/$', views.send_message_ajax, name='send_message_ajax'),
]