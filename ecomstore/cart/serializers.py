from rest_framework import serializers
from .models import CartItem
from catalog.serializers import ProductResponseSerializer


        
class ProductItemResponseSerializer(serializers.ModelSerializer):
    product = ProductResponseSerializer()

    class Meta:
        model = CartItem
        # fields = '__all__'
        fields = ('id', 'cart_id', 'quantity', 'product')


# class ProductResponseSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()
#     class Meta:
#         model = Product # this is the model that is being serialized
#         fields = ('id', 'name', 'description', 'status', 'price', 'sale_price', 'discount', 'image', 'category')