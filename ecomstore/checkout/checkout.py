from cart import cart
from .models import Order, OrderItem
from django.urls import reverse
from accounts import utils
# returns the URL from the checkout module for cart
def get_checkout_url(request):
  return reverse('checkout')

# def process(request):
#   # Transaction results
#   APPROVED = '1'
#   DECLINED = '2'
#   ERROR = '3'
#   HELD_FOR_REVIEW = '4'
#   postdata = request.POST.copy()
#   card_num = postdata.get('credit_card_number','')
#   exp_month = postdata.get('credit_card_expire_month','')
#   exp_year = postdata.get('credit_card_expire_year','')
#   exp_date = exp_month + exp_year
#   cvv = postdata.get('credit_card_cvv','')
#   amount = cart.cart_subtotal(request)
#   results = {}
#   response = authnet.do_auth_capture(amount=amount, card_num=card_num, exp_date=exp_date, card_cvv=cvv)
#   if response[0] == APPROVED:
#     transaction_id = response[6]
#     order = create_order(request, transaction_id)
#     results = {'order_number':order.id,'message':''}
#   if response[0] == DECLINED:
#     results = {'order_number':0, 'message':'There is a problem with your credit card.'}
#   if response[0] == ERROR or response[0] == HELD_FOR_REVIEW:
#     results = {'order_number':0,'message':'Error processing your order.'}
#   return results

def create_order(request) -> Order:
  order = Order()
  order.user_id = utils.user_id(request)
  order.status = Order.SUBMITTED
  order.save()
  # if the order save succeeded
  if order.pk:
    cart_items = cart.get_cart_items(request)
    for ci in cart_items:
    # create order item for each cart item
      oi = OrderItem()
      oi.order = order
      oi.quantity = ci.quantity
      oi.price = ci.product.price # now using @property
      oi.product = ci.product
      oi.save()
    # all set, empty cart
    cart.empty_cart(request)
  # return the new order object
  return order
