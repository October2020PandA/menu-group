from django.shortcuts import render, redirect
from adminPanel.models import Category, Item
from pointOfSale.models import *
from logreg.decorators import my_user_passes_test, my_login_required

@my_login_required(login_url="/login/")
def index(request):
    context = {
        'order': Order.objects.all(),
        'items': Item.objects.all(),
        'categories': Category.objects.all(),
    }
    return render(request, 'pos_home.html', context)

@my_login_required(login_url="/login/")
def add_to_order(request):
    Order.objects.create(
        
    )

@my_login_required(login_url="/login/")
def delete(request, item_id):
    pass

@my_login_required(login_url="/login/")
def checkout(request):
    Order.objects.create(

    )
    return redirect('/')