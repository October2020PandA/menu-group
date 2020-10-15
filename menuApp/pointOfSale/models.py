from django.db import models
from adminPanel.models import Item, Location
from logreg.models import User

# Create your models here.
class OrderType(models.Model):
    type_name = models.CharField(max_length=255)
    is_visible = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    order_name = models.CharField(max_length=255)
    order_discount = models.DecimalField(max_digits=7, decimal_places=3)
    order_type = models.ForeignKey(Order, related_query='orders', related_query_name='orders', on_delete=models.CASCADE)
    location = models.ForeignKey(Location, related_query='orders', related_query_name='orders', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Bill(models.Model):
    order_amount = models.DecimalField(max_digits=7, decimal_places=3)
    tax_amount = models.DecimalField(max_digits=7, decimal_places=3)
    tip_amount = models.DecimalField(max_digits=7, decimal_places=3)
    bill_amount = models.DecimalField(max_digits=7, decimal_places=3)
    sale_date = models.DateTimeField(auto_now_add=True)
    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='billAmount', related_query_name='billAmount')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderHistory(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='history', related_query_name='history')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orderHistory', related_query_name='orderHistory')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)