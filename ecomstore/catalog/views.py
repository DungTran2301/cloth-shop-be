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
      serializers = ProductResponseSerializer(products,many=True)
      return Response(serializers.data, status=status.HTTP_201_CREATED)
    except Exception as e:
      return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    



@api_view(['GET', 'POST'])
def show_category(request):
  if request.method == 'GET':
    categories = list(Category.objects.all())
    serializers = CategorySerializer(categories,many=True)
    return Response(serializers.data)


@api_view(['GET', 'POST'])
@csrf_exempt
def show_product(request, product_slug):
  product = get_object_or_404(Product, slug=product_slug)
  if request.method == 'GET':
    serializers = ProductResponseSerializer(product)
    return Response(serializers.data)
  if request.method == 'POST':
    try:
      cart.add_to_cart(request)
      if request.session.test_cookie_worked():
        request.session.delete_test_cookie()
      serializers = ProductResponseSerializer(product)

      return Response({'success': True, 'product': product.slug})
    except  Exception as e:
      return Response({'success': False, 'error': str(e)})

@api_view(['GET', 'POST'])
def search_product(request, product_slug):
  try:
    query = request.data.get('query')
    category = request.data.get('category')
    sort_by = request.data.get('sort_by')
    order = request.data.get('order')

    products = Product.objects.all()

    if query:
        products = products.filter(Q(name__icontains=query) | Q(description__icontains=query))

    if category:
        products = products.filter(category=category)

    if sort_by:
        if order == 'asc':
            products = products.order_by(sort_by)
        elif order == 'desc':
            products = products.order_by('-' + sort_by)

    serializer = ProductResponseSerializer(products, many=True)
    return Response(serializer.data, status=status.HTTP_201_CREATED)
  except Exception as e:
    return Response({"message": str(e)}, status=status.HTTP_400_BAD_REQUEST)



# new product view, with POST vs GET detection
# @api_view(['GET', 'POST'])
# def show_product(request, product_slug):
#   p = get_object_or_404(Product, slug=product_slug)
#   categories = p.categories.all()
#   page_title = p.name
#   meta_keywords = p.meta_keywords
#   meta_description = p.meta_description
#   active_categories = Category.objects.filter(is_active=True)
#   # need to evaluate the HTTP method
#   if request.method == 'POST':
#     # add to cart…create the bound form
#     postdata = request.POST.copy()
#     form = ProductAddToCartForm(request, postdata)
#     #check if posted data is valid
#     if form.is_valid():
#     #add to cart and redirect to cart page
#       cart.add_to_cart(request)
#       # if test cookie worked, get rid of it
#       if request.session.test_cookie_worked():
#         request.session.delete_test_cookie()
#       url = reverse('show_cart')
#       return HttpResponseRedirect(url) 
#   else:
#     # it’s a GET, create the unbound form. Note request as a kwarg
#     form = ProductAddToCartForm(request=request, label_suffix=':')
#   # assign the hidden input the product slug
#   form.fields['product_slug'].widget.attrs['value'] = product_slug
#   # set the test cookie on our first GET request
#   request.session.set_test_cookie()
#   return render(request, "catalog/product.html", locals()) 