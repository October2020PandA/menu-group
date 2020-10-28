from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

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

urlpatterns += staticfiles_urlpatterns()
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)