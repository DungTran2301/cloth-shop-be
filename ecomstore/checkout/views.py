from django.shortcuts import render

from django.urls import reverse
from django.http import HttpResponseRedirect
from .models import Order, OrderItem
from cart import cart
from payment.views import config
from time import time
import hmac, hashlib, urllib.parse, urllib.request
from django.shortcuts import get_object_or_404
import requests
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from accounts import utils

def receipt(request, template_name='checkout/receipt.html'):
    order_number = request.session.get('order_number', '')
    if order_number:
        order = Order.objects.filter(id=order_number)[0]
        order_items = OrderItem.objects.filter(order=order)
        del request.session["order_number"]
    else:
        cart_url = reverse('show_cart')
        return HttpResponseRedirect(cart_url)
    return render(request, template_name, locals())

@api_view(['GET'])
@csrf_exempt
def checkOrderStatus(request, order_id):
    hmac_algorithm = hashlib.sha256
    appid = config["appid"]
    key1 = config["key1"]

    order  = get_object_or_404(Order, id=order_id)
    apptransid = order.appTransId
    print(apptransid)
    hmac_input = f'{appid}|{apptransid}|{key1}'
    mac = hmac.new(key1.encode(), hmac_input.encode(), hmac_algorithm).hexdigest()

    data = {
        'appid': appid,
        'apptransid': apptransid,
        'mac': mac
    }

    print(data)
    response = requests.post("https://sandbox.zalopay.com.vn/v001/tpe/getstatusbyapptransid", data=data)
    print(response.json())
    return Response({
        'success': True,
        'code': 200,
        "message": "Get Order status Successfull",
        "data": response.json()
    }, status=status.HTTP_200_OK)

# Create your views here.
@api_view(['GET'])
def show_list_order(request):
    data_response = []
    orders = Order.objects.filter(user_id=utils.user_id(request))

    list_response = [
        {
            "id": order.pk,
            "date": order.date,
            "status": order.orderStatus,
            "order_items": [
                {
                    "id": order_item.pk,
                    "product": order_item.product.name,
                    "quantity": order_item.quantity,
                    "price": order_item.price,
                } for order_item in OrderItem.objects.filter(order=order)
            ]
        } for order in orders
    ]
    # order_items = OrderItem.objects.filter(order=order)

    return Response({
            'success': True,
            'code': 201,
            'message': 'Get orders successful!',
            'data': list_response
        }, status=status.HTTP_201_CREATED)

