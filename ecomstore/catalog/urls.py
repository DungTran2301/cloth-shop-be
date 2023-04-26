from django.urls import path, include, re_path
from . import views
urlpatterns = [
  #   'ecomstore.catalog.views',
  # path(r'^$', 'index', { 'template_name':'catalog/index.html'}, 'catalog_home'),
  # path(r'^category/(?P<category_slug>[-\w]+)/$', 
  # 'show_category', {
  # 'template_name':'catalog/category.html'},'catalog_category'),
  # path(r'^product/(?P<product_slug>[-\w]+)/$', 
  # 'show_product', {
  # 'template_name':'catalog/product.html'},'catalog_product'),
  path("", views.index),
  path("category/", views.show_category, name='category'),
  path("products/", views.show_all_product, name='products'),
  # re_path(r'^category/(?P<category_slug>[-\w]+)/$', views.show_category, name="catalog_category"),
  re_path(r'^product/(?P<product_slug>[-\w]+)/$', views.show_product, name="product"),
  re_path(r'^search/result/(?P<product_slug>[-\w]+)/$', views.search_product, name="search_product"),
]