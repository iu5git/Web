from datetime import date
from django.http import HttpResponse
from django.shortcuts import render


def hello(request):
    return render(request, "index.html", {
        'data': {
            'current_date': date.today(),
            'list': ['python', 'django', 'Swift', 'HTML', 'CSS', 'JS']
        }
    })


def get_orders(request):
    return render(request, 'orders.html', {'data': {
        'current_date': date.today(),
        'orders': [
            {'title': 'Книги с макаронами', 'id': 1},
            {'title': 'Огурцы с майонезом', 'id': 2},
            {'title': 'Куртка с дыркой', 'id': 3},
        ],
    }})


def get_order(request, order_id):
    return render(request, 'order.html', {'data': {
        'current_date': date.today(),
        'id': order_id,
    }})
