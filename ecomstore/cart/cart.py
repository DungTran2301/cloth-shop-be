from .models import CartItem
from catalog.models import Product
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect 
import decimal # not needed yet but we will later
import random
from django.conf import settings
from accounts import utils
import jwt


# CART_ID_SESSION_KEY = 'cart_id'
# # get the current user's cart id, sets new one if blank
# def _cart_id(request):
#   if request.session.get(CART_ID_SESSION_KEY,'') == '':
#     request.session[CART_ID_SESSION_KEY] = _generate_cart_id()
#   return request.session[CART_ID_SESSION_KEY]


# def _generate_cart_id():
#   cart_id = ''
#   characters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz1234567890!@#$%^&*()'
#   cart_id_length = 50
#   for y in range(cart_id_length):
#     cart_id += characters[random.randint(0, len(characters)-1)]
#   return cart_id

# return all items from the current user's cart
def get_cart_items(request):
  return CartItem.objects.filter(user_id=utils.user_id(request))

# add an item to the cart
def add_to_cart(request):
  postdata = request.data
  product_id = postdata.get('id', 0)
  quantity = postdata.get('quantity', 1)
  p = get_object_or_404(Product, id=product_id)
  cart_products = get_cart_items(request)

  product_in_cart = False

  for cart_item in cart_products:
    if cart_item.product.id == p.id:
      cart_item.augment_quantity(quantity)
      product_in_cart = True
  if not product_in_cart:
    ci = CartItem()
    ci.product = p
    ci.quantity = quantity
    ci.user_id = utils.user_id(request)
    ci.save()
  return p

# returns the total number of items in the user's cart
def cart_distinct_item_count(request):
  return get_cart_items(request).count()

def get_single_item(request, item_id):
  return get_object_or_404(CartItem, id=item_id, user_id=utils.user_id(request))

def remove_from_cart(request):
  postdata = request.data
  item_id = postdata.get('item_id')
  cart_item = get_single_item(request, item_id)
  if cart_item:
    cart_item.delete()

def cart_subtotal(request):
  cart_total = decimal.Decimal('0.00')
  cart_items = get_cart_items(request)
  
  for cart_item in cart_items:
    cart_total += cart_item.product.price * cart_item.quantity
  return cart_total

# update quantity for single item
def update_cart(request):
  postdata = request.data
  item_id = postdata.get('item_id')
  quantity = postdata.get('quantity')
  cart_item = get_single_item(request, item_id)
  if cart_item: 
    if int(quantity) > 0:
      cart_item.quantity = int(quantity)
      cart_item.save()
    else:
      remove_from_cart(request) 

def is_empty(request):
  return cart_distinct_item_count(request) == 0 

def empty_cart(request):
  user_cart = get_cart_items(request)
  user_cart.delete() 


    