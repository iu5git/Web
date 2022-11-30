
from django.conf import settings
from django.db import models
from django.utils import timezone
from authentication.models import User

class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    strength = models.IntegerField(blank=True, null=True)

    def __str__(self) -> str:
        return self.name

class Cart(models.Model):
    user = models.ForeignKey(User, models.CASCADE, related_name='cart')
    products = models.ManyToManyField(Product, verbose_name="products")

    def __str__(self) -> str:
        return self.user.get_short_name()


class Order(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now, blank=True)

    def __str__(self) -> str:
        return self.cart.user.get_short_name()
