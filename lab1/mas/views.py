from datetime import date
from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return render(request, "index.html", {
        'data': {
            'current_date': date.today(),
            'list': ['Marlboro', 'Phipip Morris', 'Parlament', 'LD', 'LM', 'Тройка', 'Ява']
        }
    })


def get_orders(request):
    return render(request, 'orders.html', {'data': {
        'current_date': date.today(),
        'orders': [
            {'title': 'Marlboro', 'id': 1},
            {'title': 'Parlament', 'id': 2},
            {'title': 'Тройка', 'id': 3},
        ],
    }})


def get_order(request, id):
    return render(request, 'order.html', {'data': {
        'current_date': date.today(),
        'id': id,
    }})
