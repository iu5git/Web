from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from tobacco_app import views



router = routers.DefaultRouter()
router.register(r'tobacco', views.TobaccoViewSet)

urlpatterns = [
    path('hello/', views.hello),
    path('products', views.ProductList),
    path('product/<int:id>/', views.get_product, name='product_url'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    path('tobacco-app', include('tobacco_app.urls')),
    path('', include(router.urls)),
    ]