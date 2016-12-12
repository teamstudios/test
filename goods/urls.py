from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^search/$', views.search_view, name='search'),
    url(r'^modal/(?P<good_pk>\d+)/$', views.goods_modal, name='goods_modal'),
    url(r'^good/(?P<good_pk>\d+)/$', views.good_view, name='good_view'),
    url(r'^add-to-wishlist/$', views.add_to_wishlist, name='add_to_wishlist'),
    url(r'^add-user-like/$', views.add_user_like, name='add_user_like'),
    url(r'^goods-filter/$',views.goods_filter, name='goods_filter'),
    url(r'^add-new-tag/$', views.add_new_tag, name='add_new_tag'),
    url(r'^add/$', views.add_good, name='add_good'),
    url(r'^edit/(?P<good_pk>\d+)/$', views.edit_good, name='edit_good'),
    url(r'^delete/(?P<pk>\d+)/$', views.GoodDeleteView.as_view(), name='delete_good'),
    url(r'^upload-good-photo/$', views.upload_good_photo, name='upload_good_photo'),
    url(r'^delete-good-photo/$', views.delete_photo, name='delete_good_photo'),
    url(r'^wishlist/$', views.show_wishlist, name='show_wishlist'),
    url(r'^add-bid/$', views.add_auction_bid, name='add_bid'),
    url(r'^remove-bid/$', views.reject_auction_bid, name='reject_bid'),
    url(r'^disable-good/$', views.set_inactive_good, name='disable-good'),
    url(r'^accept-bid/$', views.accept_bid, name='accept-bid')
]