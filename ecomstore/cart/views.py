from django.shortcuts import render
from django.template import RequestContext
from . import cart
from catalog.models import Category
from rest_framework.decorators import api_view

from django.http import HttpResponseRedirect
from checkout import checkout
from rest_framework.response import Response
from .serializers import ProductItemResponseSerializer
from rest_framework import status


from base.models import BaseResponse, GetCartItemResposeSerializer
# Create your views here.
@api_view(['GET', 'POST'])
def show_cart(request):
  if request.method == 'POST':
    postdata = request.data
    if postdata.get('submit') == 'Remove':
      cart.remove_from_cart(request)
      
    if postdata.get('submit') == 'Update':
      cart.update_cart(request)

    if postdata.get('submit') == 'Checkout':
      checkout_url = checkout.get_checkout_url(request)
      return HttpResponseRedirect(checkout_url)
  
  try:
    products = cart.get_cart_items(request)
    cart_subtotal = cart.cart_subtotal(request)
    res = BaseResponse(True, 200, "Get cart success", list(products)) 
    serializer = GetCartItemResposeSerializer(res)
    return Response(serializer.data)
  except Exception as e:
    res = BaseResponse(False, 400, str(e), None) 
    serializer = GetCartItemResposeSerializer(res)
    return Response(serializer.data)
