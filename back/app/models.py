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
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='cart',
                                related_query_name='cart_query')
    products = models.ManyToManyField(Product, verbose_name="products", blank=True)

    def __str__(self) -> str:
        return self.user.get_short_name() + 'cart'


class Order(models.Model):
    date = models.DateField(default=timezone.now, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', related_query_name='orders_query')
    products = models.ManyToManyField(Product, verbose_name="products")

    def __str__(self) -> str:
        return self.user.get_short_name() + 'order'
