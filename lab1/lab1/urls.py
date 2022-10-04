from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from tobacco_app import views
from tobacco_app.viewSets import ProductViewSet, CustomerViewSet, OrderViewSet



router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'customer', CustomerViewSet)
router.register(r'order', OrderViewSet)

urlpatterns = [
    path('hello/', views.hello),
    path('productList', views.ProductList),
    path('product/<int:id>/', views.get_product, name='product_url'),
    # path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('admin/', admin.site.urls),
    # path('tobacco-app', include('tobacco_app.urls')),
    path('', include(router.urls)),
    ]