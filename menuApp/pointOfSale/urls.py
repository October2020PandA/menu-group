from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('add_to_order', views.add_to_order, name='add_to_order'),
    path('delete', views.delete, name='delete'),
    path('checkout', views.checkout, name='checkout'),
]