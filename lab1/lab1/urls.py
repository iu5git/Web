from django.contrib import admin
from django.urls import path
from lab1 import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.get_orders),
    path('order/<int:id>/', views.get_order, name='order_url'),
]