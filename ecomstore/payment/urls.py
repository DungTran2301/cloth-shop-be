from django.urls import path, include, re_path
from . import views
urlpatterns = [
  path("bank_list/", views.paymentMethodList, name='paymentMethodList'),
  path("create_order/", views.createOrder, name='createOrder'),
  # path("products/", views.product_list, name='products'),
  # path("product/add_to_cart/", views.addToCart, name='product add to cart'),
  # re_path(r'^product/detail/(?P<id>\d+)/$', views.show_product_by_id, name="product_by_id"),
]