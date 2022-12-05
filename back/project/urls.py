from django.contrib import admin
from django.urls import include, path
from rest_framework import routers

import spectacular.urls
from tobacco_app.views import *

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='products')
router.register(r'order', OrderViewSet)
router.register(r'cart', CartViewSet)

urlpatterns = [
    path('', include(spectacular.urls)),
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include('authentication.urls', namespace='authentication')),
]
