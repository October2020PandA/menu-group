from django.urls import path, include
from . import views
# from .views import Users

urlpatterns = [
    path('', views.index, name='index'),
    path('auth', views.authenticate, name='authenticate'),
    path('register', views.register, name='register'),
    path('register/create', views.userCreate, name="userCreate"),
    path('initial-register', views.initialRegister, name='initialRegister'),
    path('initial-register/create', views.initialCreate, name="initialCreate"),
    path('location', views.location, name='location'),
    path('hours', views.openHours, name='openHours'),
    path('employee', views.employee, name='employee'),
    path('logout', views.logout, name='logout'),
    path('reset', views.clearDb, name='clearDb'),
]