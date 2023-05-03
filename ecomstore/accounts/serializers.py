
from rest_framework import serializers
from rest_framework.validators import ValidationError

from .models import User


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.CharField(max_length=80)
    username = serializers.CharField(max_length=45)
    password = serializers.CharField(min_length=2, write_only=True)
    name = serializers.CharField(max_length=45)
    role = serializers.CharField(max_length=20, default="USER")
    telephoneNumber = serializers.CharField(max_length=20)
    deliveryAddress = serializers.CharField(max_length=200)

    class Meta:
        model = User
        fields = ["email", "username", "password", "name", "role", "telephoneNumber", "deliveryAddress", "verifyToken"]

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs["email"]).exists()
        username_exitsts = User.objects.filter(username=attrs["username"]).exists()

        if email_exists:
            raise ValidationError("Email has already been used")
        if username_exitsts:
            raise ValidationError("Username has already been used")
        

        return super().validate(attrs)


class UserProfileSerializer(serializers.ModelSerializer):
     class Meta:
        model = User
        fields = ["email", "username", "name", "role", "telephoneNumber", "deliveryAddress"]