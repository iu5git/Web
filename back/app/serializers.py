from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from authentication.serializers import UserSerializer
from .models import *


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product

        fields = ["id", "name", "brand", "type", "price", "strength"]

    # def __init__(self, *args, **kwargs):
    #     # Don't pass the 'fields' arg up to the superclass
    #     fields = kwargs.pop('fields', None)
    #
    #     # Instantiate the superclass normally
    #     super().__init__(*args, **kwargs)
    #
    #     if fields is not None:
    #         # Drop any fields that are not specified in the `fields` argument.
    #         allowed = set(fields)
    #         existing = set(self.fields)
    #         for field_name in existing - allowed:
    #             self.fields.pop(field_name)


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Valid example 1',
            summary='application.json',
            description='Products id',
            value={
                'products': [1,
                             2,
                             3],
            },
            request_only=True,  # signal that example only applies to requests
            response_only=False,  # signal that example only applies to responses
        ),
    ]
)
class CartSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = Cart

        fields = ['id', "user", "products"]

        # depth = 1

    def update(self, instance, validated_data):
        product_ids = validated_data.pop('products')
        products = Product.objects.filter(pk__in=product_ids)
        instance.products.set(products)
        instance.save()

        return instance


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    products = ProductSerializer(many=True)

    class Meta:
        model = Order

        fields = ['id', "user", "date", "products", ]
