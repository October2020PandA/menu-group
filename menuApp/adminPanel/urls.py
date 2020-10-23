from django.urls import path, include
from django.conf import settings
from . import views
from django.contrib.staticfiles.urls import static # import for image files
from django.contrib.staticfiles.urls import staticfiles_urlpatterns # import for image files

urlpatterns = [
    path('', views.index, name='index'),
    # path('menu', views.index), #view all menu items
    path ('all-menu-items', views.view_items),
    path('add-menu-item', views.add_item), #add menu item to the database
    path('edit-menu-item/<int:id>', views.edit), #edit unique menu item
    path('update-menu-item/<int:id>', views.update), #update and save update after editing a menu item
    # path('delete-menu-item/<int:id>', views.destroy), #delete a menu item (removes from database)
    # path('add-category', views.fakeData, name='fakeData'), 
]