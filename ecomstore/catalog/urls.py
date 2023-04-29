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
  path("products/", views.product_list, name='products'),
  path("product/add_to_cart/", views.addToCart, name='product add to cart'),
  # re_path(r'^category/(?P<category_slug>[-\w]+)/$', views.show_category, name="catalog_category"),
  # re_path(r'^product/(?P<product_slug>[-\w]+)/$', views.show_product, name="product"),
  re_path(r'^product/detail/(?P<id>\d+)/$', views.show_product_by_id, name="product_by_id"),
]