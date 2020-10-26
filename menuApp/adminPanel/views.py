from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from adminPanel.models import *
from django.core.files.storage import FileSystemStorage # import for image files
from django.views.generic import CreateView # import for image files
from django.urls import reverse_lazy # import for image files

## may be ignored or made into landing page later, ignore for now 
def index(request): 
    # return HttpResponse('Menu Display')
    context = {
        'all_items': Item.objects.all(),
        # 'categories': Category.objects.all(),
        # 'subcategories': SubCategory.objects.all(),

    }
    return render(request, 'all-menu-items.html', context)

## ---------- CRUD MENU ITEMS ---------- ##

## Add Menu Item
def add_item(request): 
    context = {
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.all(),
    }
    return render(request, 'add-menu-item.html', context)

def create_item(request):
    if request.method == ("POST" or "FILES"):
        errors = Item.objects.item_validator(request.POST)
        if len(errors) != 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/menu-admin/add-menu-item')
        Item.objects.create(
            item_name=request.POST['item_name'], 
            item_desc=request.POST['item_desc'], 
            item_price=request.POST['item_price'], 
            item_image=request.FILES['item_image'], 
            min_calories=request.POST['min_calories'],
            max_calories=request.POST['max_calories'],
            dietary=request.POST['dietary'],
            is_available=request.POST['is_available'],
            category=Category.objects.get(id=request.POST['category']),
            subcategory=SubCategory.objects.get(id=request.POST['subcategory']),
        )
    return redirect('/menu-admin/')

## Edit Menu Item 
def edit(request, item_id):
    context = {
        'item': Item.objects.get(id=item_id),
        'categories': Category.objects.all(),
        'subcategories': SubCategory.objects.filter(category=Item.objects.get(id=item_id).category),
    }
    return render(request, 'edit-menu-item.html', context)


## Update Menu Items (after editing)
def update(request, item_id):
    if request.method == 'POST': 
        update_item = Item.objects.filter(id=item_id)
        if len(update_item) != 1:
            return redirect('/menu-admin/')
        update_item[0].item_name = request.POST['item_name']
        update_item[0].item_desc = request.POST['item_desc']
        update_item[0].item_price = request.POST['item_price']
        if 'item_image' in request.FILES:
            update_item[0].item_image = request.FILES['item_image'] ##need to review, may need to be request.FILE 
        update_item[0].min_calories = request.POST['min_calories']
        update_item[0].max_calories = request.POST['max_calories']
        update_item[0].dietary = request.POST['dietary']
        update_item[0].is_available = request.POST['is_available']
        update_item[0].category = Category.objects.get(id=request.POST['category'])
        update_item[0].subcategory = SubCategory.objects.get(id=request.POST['subcategory'])
        update_item[0].save()
    return redirect('/menu-admin/')

# Delete Menu Items 
def destroy(request, item_id):
    Item.objects.get(id=item_id).delete()
    return redirect('/menu-admin/')

## View Menu (all menu items)
def view_items(request):
    context = {
        "all_items": Item.objects.all()
        }
    return render(request, 'all-menu-items.html', context)


## ---------- UPLOAD IMAGE ---------- ##

def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage() #create object
        fs.save(uploaded_file.name, uploaded_file) #save file
        # name = fs.save()uploaded_file.name, uploaded_file)
        # context['url'] = fs.url(name)

    # UPDATE HTML LOCATION
    return render(request,'menu-dashbord.html', context) #location for this image 

def add_category(request):
    context = {
        'categories': Category.objects.all(),
    }
    return render(request, 'add-category.html', context)

def add_subcategory(request):
    context = {
        'subcategories': SubCategory.objects.all().order_by('category'),
    }
    return render(request, 'add-subcategory.html', context)

## ---------- FAKE DATA ---------- ##

## Fake data to get category and subcategory to work
def fakeData(request):
    Category.objects.create(category_name="Drinks")
    cate = Category.objects.get(category_name="Drinks")
    SubCategory.objects.create(subcategory_name="Bar", category=cate)
    SubCategory.objects.create(subcategory_name="Soda", category=cate)
    SubCategory.objects.create(subcategory_name="Wine", category=cate)
    return HttpResponse('Fake Data Added')

def view_subcategory(request):
    context = {
        'subcategories': SubCategory.objects.filter(category=Category.objects.get(id=request.POST['category_id'])),
    }
    return render(request, 'subcategory-list.html', context)

def view_item(request, item_id):
    context = {
        "item": Item.objects.get(id=item_id),
    }
    return render(request, "view_item.html", context)