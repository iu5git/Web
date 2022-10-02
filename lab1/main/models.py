from django.db import models

class Customer(models.Model):
    name = models.CharField(max_length=50)
    phone = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'customer'


class Order(models.Model):
    customer = models.ForeignKey(Customer, models.DO_NOTHING, blank=True, null=True)
    date = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'order'


class Product(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100, blank=True, null=True)
    type = models.CharField(max_length=100, blank=True, null=True)
    price = models.CharField(max_length=100, blank=True, null=True)
    strength = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product'


class ProductOrder(models.Model):
    order = models.ForeignKey(Order, models.DO_NOTHING, blank=True, null=True)
    product_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'product_order'