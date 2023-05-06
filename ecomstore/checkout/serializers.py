from rest_framework import serializers
from .models import OrderItem, Order


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        # fields = '__all__'
        fields = ('product', 'quantity', 'price')

class OrderResponseSerializer(serializers.ModelSerializer):
    orderItems = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'date', 'status', 'orderItems')