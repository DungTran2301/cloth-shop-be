from django.shortcuts import render, get_object_or_404

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse
from django.http import HttpResponseRedirect
def register(request, template_name="registration/register.html"):
  if request.method == 'POST':
    postdata = request.POST.copy()
    form = UserCreationForm(postdata)
    if form.is_valid():
      form.save()
      un = postdata.get('username','')
      pw = postdata.get('password1','')
      from django.contrib.auth import login, authenticate
      new_user = authenticate(username=un, password=pw)
      if new_user and new_user.is_active:
        login(request, new_user)
        url = reverse('my_account')
        return HttpResponseRedirect(url)
  else:
    form = UserCreationForm()
  page_title = 'User Registration'
  return render(request, template_name, locals()) 

from checkout.models import Order, OrderItem
from django.contrib.auth.decorators import login_required
@login_required
def my_account(request, template_name="registration/my_account.html"):
  page_title = 'My Account'
  orders = Order.objects.filter(user=request.user)
  print("order", orders.count())
  name = request.user.username
  return render(request, template_name, locals())

@login_required
def order_details(request, order_id, template_name="registration/order_details.html"):
  order = get_object_or_404(Order, id=order_id, user=request.user)
  page_title = 'Order Details for Order #' + order_id
  order_items = OrderItem.objects.filter(order=order)
  return render(request, template_name, locals()) 

from .forms import UserProfileForm
from . import profile
@login_required
def order_info(request, template_name="registration/order_info.html"):
  if request.method == 'POST':
    postdata = request.POST.copy()
    form = UserProfileForm(postdata)
    if form.is_valid(): 
      profile.set(request)
      url = reverse('my_account')
      return HttpResponseRedirect(url)
  else:
    user_profile = profile.retrieve(request)
    form = UserProfileForm(instance=user_profile)
  page_title = 'Edit Order Information'
  return render(request, template_name, locals()) 