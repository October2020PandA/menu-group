from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.staticfiles.urls import static # import for image files
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # import for image files

urlpatterns = [
    path('', views.index, name='index'),
    path('menu', views.menu, name='menu'),
    path('locations', views.locations, name='locations'),
    path('reservations', views.reservations, name='reservations')
]