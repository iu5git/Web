from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from tobacco_app.models import *
from tobacco_app.serializers import *
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .backends import JWTAuthentication
import redis

session_storage = redis.StrictRedis(host=settings.REDIS_HOST, port=settings.REDIS_PORT)

class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать акции компаний
    """
    # queryset всех пользователей для фильтрации по дате последнего изменения
    authentication_classes = [JWTAuthentication]
    permission_classes = (IsAuthenticated,)
    queryset = Product.objects.all().order_by('pk')
    serializer_class = ProductSerializer  # Сериализатор для модели

    def list(self, request):
        # print(authenticate(request=request))
        # try:
        #     print(request.META)
        #     token = request.META.get("token")
        #     print(token)
        #     print(session_storage.keys)
        #     print(session_storage.get(token))

        # except Exception as e:
        #       return Response("АВТОРИЗАЦИЯ", status=status.HTTP_400_BAD_REQUEST)
        # ssid = request.COOKIES["session_id"]
        # ssid = request.header
        # try:
            # session_storage.get(ssid)
            # session_storage.get()
            # session_storage.set(serializer.data.get('token'), serializer.data.get('username'))
        # except Exception as e:
        #     print(e)
        queryset = Product.objects.all()
        serializer = ProductSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'message': 'The product does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
             Product.objects.delete(pk=pk)
        # product = Product.objects.filter(pk=pk)
        except Exception as e:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)

    #     try:
    #         product = Product.objects.filter(pk=pk)
    #         product.delete()
    #     except Product.DoesNotExist:
    #         return Response({'message': 'The product does not exist'}, status=status.HTTP_404_NOT_FOUND)

    #     return Response({'message': 'Deleted'}, status=status.HTTP_200_OK)


# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint, который позволяет просматривать и редактировать акции компаний
#     """
#     # queryset всех пользователей для фильтрации по дате последнего изменения
#     queryset = User.objects.all().order_by('pk')
#     serializer_class = UserSerializer  # Сериализатор для модели

#     def list(self, request):
#         queryset = User.objects.all()
#         serializer = UserSerializer(queryset, many=True)
#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         queryset = User.objects.all()
#         customer = get_object_or_404(queryset, pk=pk)
#         serializer = UserSerializer(customer)
#         return Response(serializer.data)

#     def update(self, request, pk=None):
#         try:
#             customer = User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             return Response({'message': 'The customer does not exist'}, status=status.HTTP_404_NOT_FOUND)
#         serializer = UserSerializer(customer, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать акции компаний
    """
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = Order.objects.all().order_by('pk')
    serializer_class = OrderSerializer  # Сериализатор для модели

    def list(self, request):
        queryset = Order.objects.all()
        serializer = OrderSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Order.objects.all()
        order = get_object_or_404(queryset, pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'message': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать акции компаний
    """
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = Cart.objects.all().order_by('pk')
    serializer_class = CartSerializer  # Сериализатор для модели

    def list(self, request):
        queryset = Cart.objects.all()
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = Cart.objects.all()
        cart = get_object_or_404(queryset, pk=pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response({'message': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        try:
             Cart.objects.delete(pk=pk)
        except Exception as e:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class RegistrationAPIView(APIView):
    """
    Registers a new user.
    """
    permission_classes = [AllowAny]
    serializer_class = RegistrationSerializer

    def post(self, request):
        """
        Creates a new User object.
        Username, email, and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            {
                'token': serializer.data.get('token', None),
            },
            status=status.HTTP_201_CREATED,
        )


class LoginAPIView(APIView):
    """
    Logs in an existing user.
    """
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def post(self, request):
        """
        Checks is user exists.
        Email and password are required.
        Returns a JSON web token.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = Response(serializer.data, status=status.HTTP_200_OK)
        # response.set_cookie("session_id", value=serializer.data.get('token'))
        # session_storage.set(serializer.data.get('token'), serializer.data.get('username'))

        return response