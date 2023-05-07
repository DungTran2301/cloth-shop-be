from django.urls import path, include, re_path
from . import views
urlpatterns = [
#   (r'^$', 'show_checkout', {'template_name': 'checkout/checkout.html',
#  'SSL': settings.ENABLE_SSL }, 'checkout'),
#  (r'^receipt/$', 'receipt', {'template_name': 'checkout/receipt.html',
#  'SSL': settings.ENABLE_SSL },'checkout_receipt'), 
  # path("", views.show_checkout, name="checkout"),
  path("receipt/", views.receipt, name="checkout_receipt"),
  path("order_list/", views.show_list_order, name="show_list_order"),
  re_path(r'^order_status/(?P<order_id>\d+)/$', views.checkOrderStatus, name="order_status")
]