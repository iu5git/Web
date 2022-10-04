from .models import *
from rest_framework import serializers


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Product
        # Поля, которые мы сериализуем
        fields = ["name", "brand", "type", "price", "strength"]

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Customer
        # Поля, которые мы сериализуем
        fields = ["name", "phone", "address"]

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer
    class Meta:
        # Модель, которую мы сериализуем
        model = Order
        # Поля, которые мы сериализуем
        fields = ["customer", "date"]

class ProductOrderSerializer(serializers.ModelSerializer):
    order = OrderSerializer
    product = ProductSerializer
    class Meta:
        # Модель, которую мы сериализуем
        model = ProductOrder
        # Поля, которые мы сериализуем
        fields = ["order", "product"]