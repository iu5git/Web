from rest_framework import viewsets

from tobacco_app.serializers import *


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

    # search_fields = ['name', 'brand']

    # def get_queryset(self):
    #     queryset = self.queryset
    #     return queryset

    # def get_permissions(self):
    #     if self.action == 'list':
    #         permission_classes = [IsAuthenticatedOrReadOnly]
    #     else:
    #         permission_classes = [IsAdminUser]
    #     return [permission() for permission in permission_classes]

    # def list(self, request, *args, **kwargs):
    #     serializer = ProductSerializer(self.queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None, **kwargs):
    #     queryset = Product.objects.all()
    #     product = get_object_or_404(queryset, pk=pk)
    #     serializer = ProductSerializer(product, data=queryset)
    #     return Response(serializer.data)

    # def update(self, request, pk=None, **kwargs):
    #     try:
    #         product = Product.objects.get(pk=pk)
    #     except Product.DoesNotExist:
    #         return Response({'message': 'The product does not exist'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = ProductSerializer(product, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def destroy(self, request, pk=None, **kwargs):
    #     try:
    #         Product.objects.filter(pk=pk).delete()
    #     except Exception:
    #         return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({"status": "ok"}, status=status.HTTP_200_OK)


class OrderViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать акции компаний
    """
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = Order.objects.all().order_by('pk')
    serializer_class = OrderSerializer  # Сериализатор для модели
    #
    # def list(self, request, **kwargs):
    #     queryset = Order.objects.all()
    #     serializer = OrderSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None, **kwargs):
    #     queryset = Order.objects.all()
    #     order = get_object_or_404(queryset, pk=pk)
    #     serializer = OrderSerializer(order)
    #     return Response(serializer.data)
    #
    # def update(self, request, pk=None, **kwargs):
    #     try:
    #         order = Order.objects.get(pk=pk)
    #     except Order.DoesNotExist:
    #         return Response({'message': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = OrderSerializer(order, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def destroy(self, request, pk=None, **kwargs):
    #     try:
    #         Order.objects.filter(pk=pk).delete()
    #     except Exception:
    #         return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({"status": "ok"}, status=status.HTTP_200_OK)


class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint, который позволяет просматривать и редактировать акции компаний
    """
    # queryset всех пользователей для фильтрации по дате последнего изменения
    queryset = Cart.objects.all().order_by('pk')
    serializer_class = CartSerializer  # Сериализатор для модели

    # def list(self, request, **kwargs):
    #     queryset = Cart.objects.all()
    #     serializer = CartSerializer(queryset, many=True)
    #     return Response(serializer.data)
    #
    # def retrieve(self, request, pk=None, **kwargs):
    #     queryset = Cart.objects.all()
    #     cart = get_object_or_404(queryset, pk=pk)
    #     serializer = CartSerializer(cart)
    #     return Response(serializer.data)
    #
    # def update(self, request, pk=None, **kwargs):
    #     try:
    #         cart = Cart.objects.get(pk=pk)
    #     except Cart.DoesNotExist:
    #         return Response({'message': 'The order does not exist'}, status=status.HTTP_404_NOT_FOUND)
    #     serializer = CartSerializer(cart, data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    #
    # def destroy(self, request, pk=None, **kwargs):
    #     try:
    #         Cart.objects.filter(pk=pk).delete()
    #     except Exception:
    #         return Response(self.serializer_class.errors, status=status.HTTP_400_BAD_REQUEST)
    #     return Response({"status": "ok"}, status=status.HTTP_200_OK)
