from django.shortcuts import render, redirect, HttpResponse
from adminPanel.models import *
from django.core.files.storage import FileSystemStorage # import for image files
from django.views.generic import CreateView # import for image files
from django.urls import reverse_lazy # import for image files
from adminPanel.models import Category, Location

# Create your views here.
def index(request):
    context = {
        'categories': Category.objects.all(),
        'locations': Location.objects.all(),
    }
    return render(request, 'home.html', context)

def menu(request):
    context = {
        'categories': Category.objects.all(),
        'locations': Location.objects.all(),
    }
    return render(request, 'menu.html', context)

def locations(request):
    context = {
        'categories': Category.objects.all(),
        'locations': Location.objects.all(),
    }
    return render(request, 'locations.html', context)

def reservations(request):
    context = {
        'categories': Category.objects.all(),
        'locations': Location.objects.all(),
    }
    return render(request, 'reservations.html', context)
