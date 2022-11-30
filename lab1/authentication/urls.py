from django.urls import path, re_path, include
from rest_framework import routers


from .views import *

app_name = 'authentication'

urlpatterns = [
    path('registration/', RegistrationAPIView.as_view()),
    path('login/', LoginAPIView.as_view()),
    path('user/', UserRetrieveUpdateAPIView.as_view()),
]