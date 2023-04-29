from rest_framework import serializers
from .models import Category, Product


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category # this is the model that is being serialized
        fields = '__all__'
        # fields = ('id', 'name', 'description',
        #           'slug', 'is_active', 'created_at', 'updated_at')

class CategoryResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Category # this is the model that is being serialized
        fields = ('id', 'name')
        
class ProductResponseSerializer(serializers.ModelSerializer):
    categories = CategoryResponseSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        # fields = '__all__'
        fields = ('id', 'name', 'supplier', 'price'
                  , 'old_price', 'discount', 'image', 'description', 'categories')
        
# class ProductResponseSerializer(serializers.ModelSerializer):
#     category = CategorySerializer()
#     class Meta:
#         model = Product # this is the model that is being serialized
#         fields = ('id', 'name', 'description', 'status', 'price', 'sale_price', 'discount', 'image', 'category')