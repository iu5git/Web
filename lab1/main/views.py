from datetime import date
from django.http import HttpResponse
from django.shortcuts import render
from main.models import Product


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
