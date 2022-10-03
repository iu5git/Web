from django.urls import re_path
from .views import ListView

urlpatterns = [
  re_path(r"^(?P<api_name>[a-z]+)", ListView, name='tobacco-objects'),
]