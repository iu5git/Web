from rest_framework import serializers

from authentication.serializers import UserSerializer
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = ["id", "name", "brand", "type", "price", "strength"]


class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer
    products = ProductSerializer

    class Meta:
        model = Cart

        fields = ['id', "user", "products"]
        # depth = 1


class OrderSerializer(serializers.ModelSerializer):
    cart = CartSerializer

    class Meta:
        model = Order

        fields = ['id', "cart", "date"]
