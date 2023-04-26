from django.urls import path, include, re_path
from . import views
urlpatterns = [
  path("", views.get_product_comment, name='comment'),
  path("create", views.create_comment, name='create_comment'),
  # path("products/", views.show_all_product, name='products'),
  # re_path(r'^category/(?P<category_slug>[-\w]+)/$', views.show_category, name="catalog_category"),
  # re_path(r'^product/(?P<product_slug>[-\w]+)/$', views.show_product, name="product"),
]