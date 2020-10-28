from django.contrib import admin
from .models import OnlineOrder, OrderItem
from adminPanel.models import Item

admin.site.register(OnlineOrder)
admin.site.register(OrderItem)
admin.site.register(Item)
