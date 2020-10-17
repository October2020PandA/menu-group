from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('location', views.location, name='location'),
    path('hours', views.openHours, name='openHours'),
]