from rest_framework.response import Response
from rest_framework import serializers
from django.db import models
from catalog.serializers import ProductResponseSerializer, CategoryResponseSerializer
from cart.serializers import ProductItemResponseSerializer
import json

class BaseResponse:
    def __init__(self, success, code, message, data=None):
        self.success = success
        self.code = code
        self.message = message
        self.data = data
            

    def as_response(self):
        response = {'success': self.success, 'code': self.code, 'message': self.message, 'data': json.dumps(self.data)}
        return response

class GetProductResposeSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    code = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        if isinstance(obj.data, list):
            return [ProductResponseSerializer(item).data for item in obj.data]
        elif isinstance(obj.data, dict):
            return serializers.DictField().to_representation(obj.data)
        else:
            return ProductResponseSerializer(obj.data).data

    def create(self, validated_data):
        return BaseResponse(**validated_data)

    def update(self, instance, validated_data):
        instance.success = validated_data.get('success', instance.success)
        instance.code = validated_data.get('code', instance.code)
        instance.message = validated_data.get('message', instance.message)
        instance.data = validated_data.get('data', instance.data)
        return instance
    
class GetCartItemResposeSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    code = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        if isinstance(obj.data, list):
            return [ProductItemResponseSerializer(item).data for item in obj.data]
        elif isinstance(obj.data, dict):
            return serializers.DictField().to_representation(obj.data)
        else:
            return ProductItemResponseSerializer(obj.data).data

    def create(self, validated_data):
        return BaseResponse(**validated_data)

    def update(self, instance, validated_data):
        instance.success = validated_data.get('success', instance.success)
        instance.code = validated_data.get('code', instance.code)
        instance.message = validated_data.get('message', instance.message)
        instance.data = validated_data.get('data', instance.data)
        return instance
    
class GetCategoryResposeSerializer(serializers.Serializer):
    success = serializers.BooleanField()
    code = serializers.IntegerField()
    message = serializers.CharField()
    data = serializers.SerializerMethodField()

    def get_data(self, obj):
        if isinstance(obj.data, list):
            return [CategoryResponseSerializer(item).data for item in obj.data]
        elif isinstance(obj.data, dict):
            return serializers.DictField().to_representation(obj.data)
        else:
            return CategoryResponseSerializer(obj.data).data

    def create(self, validated_data):
        return BaseResponse(**validated_data)

    def update(self, instance, validated_data):
        instance.success = validated_data.get('success', instance.success)
        instance.code = validated_data.get('code', instance.code)
        instance.message = validated_data.get('message', instance.message)
        instance.data = validated_data.get('data', instance.data)
        return instance