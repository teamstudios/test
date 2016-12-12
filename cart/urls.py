from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^add-to-cart/$', views.add_to_cart, name='add_to_cart'),
    url(r'^cart-detail/$', views.cart_detail, name='cart_detail'),
    url(r'^remove-from-cart/$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^showcase-detail/$', views.show_showcase, name='showcase_detail'),
]