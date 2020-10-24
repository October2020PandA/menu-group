from django.shortcuts import render, redirect, HttpResponse
from .models import *
from logreg.models import User, Group, Permission
from adminPanel.models import Location, LocationHour, Item, ItemOption, Category, SubCategory, ItemOption
from pointOfSale.models import Order, OrderType, OrderHistory, Bill
from datetime import datetime
import stripe

stripe.api_key = "sk_test_51HaCGMEF86nHrkFh9YWAwMtKJU8JvLbFgaOtc2Kt4vYsY20R8CPmT5x69w25VbFqPZXuA2AMAPgR6S4oYBdtCe9Y00QkFFoZvZ"

# Create your views here.
def index(request):
    context = {
        'items': Item.objects.all(),
        'locations': Location.objects.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'order.html', context)

def items(request):
    pass

def cart(request):
    pass

def updateItem(request):
    pass

def processOrder(request):
    pass

def charge(request):
    if request.method == 'POST':
        print('Data:', request.POST)

        amount = 1

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
    return render(request, 'checkout.html')

def success(request):
    return render(request, 'success.html')

def logout(request):
    request.session.flush()
    return redirect('/')

