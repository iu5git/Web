from datetime import date
from django.shortcuts import render
from rest_framework import viewsets

from django.shortcuts import get_object_or_404
from rest_framework import  status
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from django.conf import settings

# Connect to our Redis instance


from .models import *
from .serializers import *


def hello(request):
    return render(request, "index.html", {
        'data': {
            'current_date': date.today(),
            'list': ['Marlboro', 'Phipip Morris', 'Parlament', 'LD', 'LM', 'Тройка', 'Ява']
        }
    })


def ProductList(request):
    return render(request, 'productList.html', {'data': {
        'current_date': date.today(),
        'products': Product.objects.all()
    }})


def get_product(request, id):
    return render(request, 'product.html', {'data': {
        'current_date': date.today(),
        'product': Product.objects.filter(id=id)[0]
    }})

# nt = namedtuple("object", ["model", "serializers"])
# pattern = {
#     "product"  : nt(Product, ProductSerializer),
#     "customer"  : nt(Customer, CustomerSerializer),
#     "order"   : nt(Order, OrderSerializer),
#     "product_order": nt(ProductOrder, ProductOrderSerializer),
# }

# @api_view(["GET", "POST"])
# def ListView(request, api_name):
#     object =  pattern.get(api_name, None)
#     if object == None:
#         return Response(
#             data   = "Invalid URL",
#             status = status.HTTP_404_NOT_FOUND,
#         )
#     if request.method == "GET":
#         object_list = object.model.objects.all()
#         serializers = object.serializers(object_list, many=True)
#         return Response(serializers.data)

#     if request.method == "POST":
#         data = request.data
#         serializers = object.serializers(data=data)

#         if not serializers.is_valid():
#             return Response(
#                 data   = serializers.error,
#                 status = status.HTTP_404_NOT_FOUND
#             )
#         serializers.save()
#         return Response(
#                 data   = serializers.error,
#                 status = status.HTTP_201_CREATED
#         )