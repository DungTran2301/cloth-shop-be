from django.shortcuts import render

from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_protect, csrf_exempt
from time import time
import hmac, hashlib, urllib.parse, urllib.request
from rest_framework import status
from rest_framework.response import Response
import requests
import json
import datetime
import time

from checkout.serializers import OrderItemSerializer

import checkout.checkout as cu
from checkout.models import OrderItem
# Create your views here.

sandboxUrl = "https://sandbox.zalopay.com.vn/v001/tpe/createorder"


config = {
  "appid": 554,
  "key1": "8NdU5pG5R2spGHGhyO99HN1OhD8IQJBn",
  "key2": "uUfsWgfLkRLzq6W2uNXTCxrfxs51auny",
  "endpoint": "https://sbgateway.zalopay.vn/api/getlistmerchantbanks"
}

@api_view(['GET'])
@csrf_exempt
def paymentMethodList(request):

    reqtime = int(round(time() * 1000)) # miliseconds
    data = "{}|{}".format(config["appid"], reqtime) # appid|reqtime

    params = {
        "appid": config["appid"],
        "reqtime": reqtime,
        "mac": hmac.new(config['key1'].encode(), data.encode(), hashlib.sha256).hexdigest()
    }

    response = urllib.request.urlopen(url=config["endpoint"], data=urllib.parse.urlencode(params).encode())
    result = json.loads(response.read())

    print("returncode: {}".format(result["returncode"]))
    print("returnmessage: {}".format(result["returnmessage"]))

    list_response = [{"pmcid": pmcid, "bank": bank} for pmcid, banklist in result["banks"].items() for bank in banklist]

    return Response({
        'success': True,
        'code': 200,
        "message": "Get Profile Successfull",
        "data": list_response
    }, status=status.HTTP_200_OK)
    # for pmcid, banklist in result["banks"].items():
    #     for bank in banklist:
    #         print("{}. {}".format(pmcid, bank))


@api_view(['POST'])
@csrf_exempt
def createOrder(request):
    appid = config["appid"]
    appuser = request.data.get('appuser', '')
    embeddata = request.data.get('embeddata', '')
    description = request.data.get('description', '')
    order = cu.create_order(request)
    orderid = order.pk
    order_items = OrderItem.objects.filter(order=order)
    item = [OrderItemSerializer(item).data for item in order_items] 
    amount = int(order.total)

    current_date = datetime.datetime.now()
    formatted_date = current_date.strftime('%y%m%d')

    apptransid = f'{formatted_date}_{orderid}'

    current_time_ms = int(round(time.time() * 1000))

    hmac_algorithm = hashlib.sha256
    key1 = config["key1"]
    hmac_input = f'{appid}|{apptransid}|{appuser}|{amount}|{current_time_ms}|{embeddata}|{item}'
    mac = hmac.new(key1.encode(), hmac_input.encode(), hmac_algorithm).hexdigest()

    data = {
        'appid': appid,
        'apptransid': apptransid,
        'appuser': appuser,
        'apptime': current_time_ms,
        'description': description,
        'embeddata': embeddata,
        'item': str(item),
        'amount': amount,
        'mac': mac
    }

    print(data)
    response = requests.post(sandboxUrl, data=data)

    data_response = {
        'orderId': orderid,
        'createOrderResponse': response.json()
    }
    return Response({
            'success': True,
            'code': 201,
            'message': 'Create payment successful!',
            'data': data_response
        }, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@csrf_exempt
def callback(request):
    result = {}
    try: 
        cbdata  = request.data
        mac = hmac.new(config['key2'].encode(), cbdata.get('data').encode(), hashlib.sha256).hexdigest()
        if mac != cbdata.get('mac'):
            # callback không hợp lệ
            result['returncode'] = -1
            result['returnmessage'] = 'mac not equal'
        else:
            # thanh toán thành công
            # merchant cập nhật trạng thái cho đơn hàng
            dataJson = json.loads(cbdata.get('data'))
            print("update order's status = success where apptransid = " + dataJson['apptransid'])

            result['returncode'] = 1
            result['returnmessage'] = 'success'
    except Exception as e:
        result['returncode'] = 0 # ZaloPay server sẽ callback lại (tối đa 3 lần)
        result['returnmessage'] = str(e)
    return Response(result)

@api_view(['GET'])
@csrf_exempt
def redirect(request):
    data = request.args
    checksumData = "{}|{}|{}|{}|{}|{}|{}".format(data.get('appid'), data.get('apptransid'), data.get('pmcid'), data.get('bankcode'), data.get('amount'), data.get('discountamount'), data.get('status'))
    checksum = hmac.new(config['key2'].encode(), checksumData, hashlib.sha256).hexdigest()

    if checksum != data.get('checksum'):
        return "Bad Request", 400
    else:
        
        return "Ok", 200