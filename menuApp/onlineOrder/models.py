from django.db import models
from adminPanel.models import Location, LocationHour, Category, SubCategory, Item, ItemOption
from logreg.models import *
from pointOfSale.models import *
import re 

class OnlineOrder(models.Model):
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)

    @property
    def get_cart_total(self):
        orderitems = self.OnlineOrderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.OnlineOrderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total


class OrderItem(models.Model):
    item = models.ForeignKey(Item, on_delete=models.SET_NULL, null=True, blank=True)
    OnlineOrder = models.ForeignKey(OnlineOrder, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total


