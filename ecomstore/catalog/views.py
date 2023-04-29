from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404
from .models import Category, Product
from django.template import RequestContext
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import CategorySerializer, ProductResponseSerializer
from rest_framework import status
from cart import cart
from django.db.models import Q
from .forms import ProductAddToCartForm
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json
from django.http import JsonResponse
from base.models import BaseResponse, GetProductResposeSerializer


def index(request, template_name="catalog/index.html"):
    page_title = 'Musical Instruments and Sheet Music for Musicians'
    active_categories = Category.objects.filter(is_active=True)
    return render(request, template_name, locals())


# def show_category(request, category_slug, template_name="catalog/category.html"):
#   c = get_object_or_404(Category, slug=category_slug)
#   products = c.product_set.all()
#   page_title = c.name
#   meta_keywords = c.meta_keywords
#   meta_description = c.meta_description
#   active_categories = Category.objects.filter(is_active=True)
#   return render(request, template_name, locals())
@api_view(['GET'])
def show_all_product(request):
    if request.method == 'GET':
        products = list(Product.objects.all())
        try:
            serializers = ProductResponseSerializer(products, many=True)
            return Response(serializers.data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def show_category(request):
    if request.method == 'GET':
        categories = list(Category.objects.all())
        serializers = CategorySerializer(categories, many=True)
        return Response(serializers.data)


@api_view(['GET', 'POST'])
@csrf_exempt
def addToCart(request):
    if request.method == 'POST':
        try:
            product = cart.add_to_cart(request)
            if request.session.test_cookie_worked():
                request.session.delete_test_cookie()
            res = BaseResponse(True, 200, "success", product) 
            serializer = GetProductResposeSerializer(res)
            return Response(serializer.data)
        except Exception as e:
            res = BaseResponse(False, 400, str(e), None) 
            serializer = GetProductResposeSerializer(res)
            return Response(serializer.data)

@api_view(['GET'])
@csrf_exempt
def show_product_by_id(request, id):
    product = get_object_or_404(Product, id=id)
    if request.method == 'GET':
        res = BaseResponse(True, 200, "success", product) 
        serializer = GetProductResposeSerializer(res)
        return Response(serializer.data)


@api_view(['POST'])
@csrf_exempt
def product_list(request):
    if request.method == 'POST':
        key_word = request.data.get('key_word', '')
        order_by_price = request.data.get('order_by_price', '')
        list_category = request.POST.getlist('list_category', [])
        price_from = request.data.get('price_from', '')
        price_to = request.data.get('price_to', '')
        products = Product.objects.all()

        if key_word:
            products = products.filter(name__icontains=key_word)

        if order_by_price:
            if order_by_price == 'asc':
                products = products.order_by('price')
            elif order_by_price == 'desc':
                products = products.order_by('-price')

        # if list_category:
        # # Filter products by category
        #     products = [p for p in products if p.categories in list_category]
        #     products = products.filter(category__in=list_category)

        if price_from:
            products = products.filter(price__gte=price_from)

        if price_to:
            products = products.filter(price__lte=price_to)
        
        try:
            listp = list(products)
            res = BaseResponse(True, 200, "Get product success", listp) 
            serializer = GetProductResposeSerializer(res)
            return Response(serializer.data)#Response(response_data, safe=False)
        except Exception as e:
            res = BaseResponse(False, 400, str(e), None) 
            serializer = GetProductResposeSerializer(res)
            return Response(serializer.data)

