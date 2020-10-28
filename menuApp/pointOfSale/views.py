from django.shortcuts import render, redirect
from adminPanel.models import Category, Item
from pointOfSale.models import *


def index(request):
    context = {
        'order': Order.objects.all(),
        'items': Item.objects.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'pos_home.html', context)

def add_to_order(request):
    Order.objects.create(
        
    )

def delete(request, item_id):
    pass

def checkout(request):
    Order.objects.create(

    )
    return redirect('/')