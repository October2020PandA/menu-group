from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('locations', views.locations, name='locations'),
    path('reservations', views.reservations, name='reservations')
]