from django.shortcuts import render, redirect, HttpResponse

# Create your views here.
def index(request):
    return render(request, 'home.html')

def menu(request):
    return render(request, 'menu.html')

def locations(request):
    return render(request, 'locations.html')

def reservations(request):
    return render(request, 'reservations.html')