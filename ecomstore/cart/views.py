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

    serializers = ProductItemResponseSerializer(products, many=True)
    return Response({'total_amount': cart_subtotal, 'items': serializers.data}, status=status.HTTP_201_CREATED)
  except Exception as e:
    return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
