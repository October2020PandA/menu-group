from django.shortcuts import render, redirect, HttpResponse
from .models import *
from datetime import datetime

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
    pass

def checkout(request):
    return render(request, 'checkout.html')

def logout(request):
    request.session.flush()
    return redirect('/')







