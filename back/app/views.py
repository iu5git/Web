from drf_spectacular.utils import extend_schema
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from app.serializers import *


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать товары
    """
    # queryset всех пользователей для фильтрации по дате последнего изменения
    # permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = Product.objects.all()
    serializer_class = ProductSerializer  # Сериализатор для модели
    filterset_fields = ('name', 'brand', 'price', 'strength',)
    search_fields = ['^name', '^brand', 'price']
    ordering_fields = ['name', 'brand']
    ordering = ['name']

    def get_permissions(self):
        if self.action == 'list' or self.action == 'retrieve' and self.detail:
            permission_classes = [IsAuthenticatedOrReadOnly]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    def list(self, request, *args, **kwargs):
        serializer = ProductSerializer(self.filter_queryset(self.queryset), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Product.objects.all()
        product = get_object_or_404(queryset, pk=pk)
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, pk=None, **kwargs):
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            return Response({'message': 'The product does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ProductSerializer(product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        try:
            Product.objects.filter(pk=pk).delete()
        except Exception:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать заказы пользователей
    """
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = Order.objects.all()
    serializer_class = OrderSerializer  # Сериализатор для модели
    filterset_fields = ('user__id',)
    ordering_fields = ['date']
    ordering = ['-date']

    def get_permissions(self):
        if self.action == 'get_orders' or self.action == 'create_new_order':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @extend_schema(
        filters=True,
    )
    @action(detail=False, methods=['get'])
    def get_orders(self, request):
        request_user = request.user
        user = User.objects.get(pk=request_user.pk)
        try:
            orders = self.filter_queryset(self.queryset)
            orders = orders.filter(user__pk=user.pk)

            order_serializer = OrderSerializer(orders, many=True)
            return Response(order_serializer.data)
        except:
            return Response([], status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def create_new_order(self, request):
        request_user = request.user
        user = User.objects.get(pk=request_user.pk)

        cart = Cart.objects.get(user=user)
        order = Order(user=user, date=timezone.now())
        order.save()
        products = cart.products.all()
        order.products.set(products)
        order.save()
        order_serialized = OrderSerializer(order)
        cart.products.clear()
        cart.save()
        return Response(order_serialized.data, status=status.HTTP_200_OK)

    def list(self, request, **kwargs):
        queryset = Order.objects.all()
        serializer = OrderSerializer(self.filter_queryset(self.queryset), many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        order = get_object_or_404(self.filter_queryset(self.queryset), pk=pk)
        serializer = OrderSerializer(order)
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return Response({'message': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = OrderSerializer(order, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, pk=None, **kwargs):
        try:
            Order.objects.filter(pk=pk).delete()
        except Exception:
            return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"status": "ok"}, status=status.HTTP_200_OK)


class CartViewSet(viewsets.GenericViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать корзину пользователя
    """
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = Cart.objects.all()
    serializer_class = CartSerializer  # Сериализатор для модели

    def get_permissions(self):
        if self.action == 'get_cart' or self.action == 'change_products':
            permission_classes = [IsAuthenticated]
        else:
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'])
    def get_cart(self, request):
        request_user = request.user
        user = User.objects.get(pk=request_user.pk)
        try:
            cart = Cart.objects.get(user__pk=user.pk)
            cart_serializer = CartSerializer(cart)
            return Response(cart_serializer.data)
        except:
            return Response([], status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['post'])
    def change_products(self, request):
        request_user = request.user
        user = User.objects.get(pk=request_user.pk)
        cart = user.get_cart()
        cart_serializer = CartSerializer(partial=True)
        new_cart = cart_serializer.update(cart, request.data)
        return Response(CartSerializer(new_cart).data, status=status.HTTP_200_OK)

    def list(self, request, **kwargs):
        queryset = Cart.objects.all()
        serializer = CartSerializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, **kwargs):
        queryset = Cart.objects.all()
        cart = get_object_or_404(queryset, pk=pk)
        serializer = CartSerializer(cart)
        return Response(serializer.data)

    def update(self, request, pk=None, **kwargs):
        try:
            cart = Cart.objects.get(pk=pk)
        except Cart.DoesNotExist:
            return Response({'message': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND)
        serializer = CartSerializer(cart, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# def destroy(self, request, pk=None, **kwargs):
#     try:
#         Cart.objects.filter(pk=pk).delete()
#     except Exception:
#         return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
#     return Response({"status": "ok"}, status=status.HTTP_200_OK)
