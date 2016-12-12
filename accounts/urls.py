from django.conf.urls import url

from django.contrib.auth import views as django_views

from . import views

urlpatterns = [
    url(r'^registration/$', views.registration_page, name='registration'),
    url(r'^activation/(?P<token>[\w]+)/$', views.activation_view, name='activation'),
    url(r'^password-reset-link/(?P<token>[\w]+)/$', views.activation_view, name='password_reset_link'),
    url(r'^profile/$', views.profile_view, name='profile'),
    url(r'^login/$', django_views.login, name='login'),
    url(r'^logout/$', django_views.logout, name='logout'),
    url(r'^restore/$', views.restore_password, name='restore_password'),
    url(r'^restore-send-email/$', views.restore_send_email, name='restore_send_email'),
    # url(r'^password-reset-link/(?P<token>[\w]+)/$', views.password_reset_link, name='password_reset_link'),
    url(r'^restore-send-sms/$', views.restore_send_sms, name='restore_send_sms'),
    url(r'^password_confirm_code/$', views.password_confirm_code, name='password_confirm_code'),
    # url(r'^password-reset-email/done/$', django_views.password_reset_done, name='password_reset_done'),
    url(r'^logout-then-login/$', django_views.logout_then_login, name='logout_then_login'),
    url(r'^reset-password/$', views.reset_password, name='reset_password'),
    url(r'^add-subscriber/$', views.add_subscriber, name='add_subscriber'),
    url(r'^upload-image/$', views.upload_image, name='upload_image'),
    url(r'^add-review/$', views.add_review, name='add_review'),
    url(r'^show-subscriptions/$', views.show_subscriptions, name='show_subscriptions'),
    url(r'^user-search/$', views.user_search, name='user_search'),
    url(r'^snap-card/$', views.snap_card, name='snap_card')
]