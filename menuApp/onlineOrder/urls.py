from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('checkout', views.checkout, name="checkout"),
    path('logout', views.logout, name='logout')
]