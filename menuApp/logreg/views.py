from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def index(request):
    context = {
        'title': 'Menu Registration',
    }
    return render(request, 'main_login.html', context)

def register(request):
    context = {
        'title': 'Menu Registration',
    }
    return render(request, 'main_login.html', context)

def location(request):
    context = {
        'cardHeader': 'Add Main Location',
    }
    return render(request, 'add_location.html', context)

def openHours(request):
    context = {
        'cardHeader': 'Add Restaurant Hours',
    }
    return render(request, 'add_hours.html', context)