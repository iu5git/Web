from django.contrib import admin
from django.urls import include, path, re_path
from rest_framework import routers
from tobacco_app import views
from tobacco_app.views import *



router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'order', OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include(router.urls)),
    path('', include('authentication.urls', namespace='authentication')),
    ]