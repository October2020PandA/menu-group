from django.shortcuts import render, redirect, HttpResponse
from .models import *
from logreg.models import User, Group, Permission
from adminPanel.models import Location, LocationHour, Item, ItemOption, Category, SubCategory, ItemOption
from pointOfSale.models import Order, OrderType, OrderHistory, Bill
from datetime import datetime
import stripe
from django.http import JsonResponse
import json
from django.core.files.storage import FileSystemStorage # import for image files
from django.views.generic import CreateView # import for image files
from django.urls import reverse_lazy # import for image files
from django.views.decorators.csrf import csrf_exempt

stripe.api_key = "sk_test_51HaCGMEF86nHrkFh9YWAwMtKJU8JvLbFgaOtc2Kt4vYsY20R8CPmT5x69w25VbFqPZXuA2AMAPgR6S4oYBdtCe9Y00QkFFoZvZ"

# Create your views here.
def index(request):
    order, created = OnlineOrder.objects.get_or_create(complete=False)
    cartItems = OnlineOrder.get_cart_items
    context = {
        'categories': Category.objects.all(),
        'items': Item.objects.all(),
        'order': order,
        'cartItems': cartItems,
    }
    return render(request, 'order.html', context)

def items(request):
    pass

def cart(request):
    order, created = OnlineOrder.objects.get_or_create(complete=False)
    items = order.orderitem_set.all()
    cartItems = OnlineOrder.get_cart_items
    context = {
        'items': items,
        'order': order,
        'cartItems': cartItems,

    }
    return redirect('/order-online')

@csrf_exempt
def updateItem(request):
    data = json.loads(request.body)
    itemId = data['itemId']
    action = data['action']

    print('Action:', action)
    print('itemId:', itemId)

    item = Item.objects.filter(id=itemId)
    order, created = OnlineOrder.objects.get_or_create(id=itemId, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(OnlineOrder=OnlineOrder, item=item)

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def processOrder(request):
    pass

def charge(request):
    if request.method == 'POST':
        print('Data:', request.POST)

        amount = 36

        customer = stripe.Customer.create(
            name = request.POST['name'],
            source = request.POST['stripeToken'],
        )

        charge = stripe.Charge.create(
            customer = customer,
            amount = amount*100,
            currency = 'usd',
            description = 'food'
        )
    return redirect('/order-online/success')


def checkout(request):
    context = {
        'items': Item.objects.all(),
    }
    return render(request, 'checkout.html', context)

def success(request):
    return render(request, 'success.html')

def logout(request):
    request.session.flush()
    return redirect('/')

