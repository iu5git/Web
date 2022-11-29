from .models import *
from rest_framework import serializers
from .backends import *
from django.contrib.auth import authenticate, login

class RegistrationSerializer(serializers.ModelSerializer):
    """
    Creates a new user.
    Email, username, and password are required.
    Returns a JSON web token.
    """

    # The password must be validated and should not be read by the client
    password = serializers.CharField(
        max_length=128,
        min_length=4,
        write_only=True,
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ('email', 'username', 'password', 'token',)

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.Serializer):
    """
    Authenticates an existing user.
    Email and password are required.
    Returns a JSON web token.
    """
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(max_length=128, write_only=True)

    # Ignore these fields if they are included in the request.
    username = serializers.CharField(max_length=255, read_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        """
        Validates user data.
        """
        email = data.get('email', None)
        password = data.get('password', None)

        if email is None:
            raise serializers.ValidationError(
                'An email address is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )
        user = authenticate(email=email, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this email and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'token': user.token,
            'username': user.get_username
        }


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        # Модель, которую мы сериализуем
        model = Product
        # Поля, которые мы сериализуем
        fields = ["id", "name", "brand", "type", "price", "strength"]

class OrderSerializer(serializers.ModelSerializer):
    user = LoginSerializer

    class Meta:
        # Модель, которую мы сериализуем
        model = Order
        # Поля, которые мы сериализуем
        fields = ['id', "user", "date"]

class CartSerializer(serializers.ModelSerializer):
    uset = LoginSerializer
    products = ProductSerializer
    class Meta:
        model = Cart

        fields = ['id', "user", "products"]

# class ProductOrderSerializer(serializers.ModelSerializer):
#     order = OrderSerializer
#     product = ProductSerializer
#     class Meta:
#         # Модель, которую мы сериализуем
#         model = ProductOrder
#         # Поля, которые мы сериализуем
#         fields = ["order", "product"]


