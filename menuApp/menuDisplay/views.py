from django.shortcuts import render, redirect, HttpResponse
from adminPanel.models import *
from django.core.files.storage import FileSystemStorage # import for image files
from django.views.generic import CreateView # import for image files
from django.urls import reverse_lazy # import for image files

# Create your views here.
def index(request):
    return render(request, 'home.html')

def menu(request):
    return render(request, 'menu.html')

def locations(request):
    return render(request, 'locations.html')

def reservations(request):
    return render(request, 'reservations.html')
