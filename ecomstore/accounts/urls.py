from django.urls import path, include, re_path
from . import views
from ecomstore import settings
from django.contrib.auth import views as auth_view

# urlpatterns = patterns('ecomstore.accounts.views',
#  (r'^register/$', 'register',
#  {'template_name': 'registration/register.html', 'SSL': settings.ENABLE_SSL },
# 'register'),
#  (r'^my_account/$', 'my_account',
#  {'template_name': 'registration/my_account.html'}, 'my_account'),
#  (r'^order_details/(?P<order_id>[-\w]+)/$', 'order_details',
#  {'template_name': 'registration/order_details.html'}, 'order_details'),
#  (r'^order_info//$', 'order_info',
#  {'template_name': 'registration/order_info.html'}, 'order_info'),
# )
# urlpatterns += patterns('django.contrib.auth.views',
#  (r'^login/$', 'login', {'template_name': 'registration/login.html', 'SSL':
# settings.ENABLE_SSL }, 'login'),
# ) 
urlpatterns = [
  path('register/', views.register, name="register"),
  path('my_account/', views.my_account, name="my_account"),
  re_path(r'^order_details/(?P<order_id>[-\w]+)/$', views.order_details, name="order_details"),
  path('order_info/', views.order_info, name="order_info"),
]