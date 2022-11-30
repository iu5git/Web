from authentication.serializers import LoginSerializer
from .models import *
from rest_framework import serializers

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = ["id", "name", "brand", "type", "price", "strength"]


class OrderSerializer(serializers.ModelSerializer):
    user = LoginSerializer

    class Meta:
        model = Order

        fields = ['id', "user", "date"]


class CartSerializer(serializers.ModelSerializer):
    uset = LoginSerializer
    products = ProductSerializer

    class Meta:
        model = Cart

        fields = ['id', "user", "products"]
