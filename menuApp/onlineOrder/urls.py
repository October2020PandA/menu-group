from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('items', views.items),
    path('cart', views.cart),
    path('update_item', views.updateItem),
    path('process_order', views.processOrder),
    path('charge', views.charge),
    path('checkout', views.checkout, name="checkout"),
    path('success', views.success),
    path('logout', views.logout, name='logout'),
]