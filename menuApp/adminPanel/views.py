from django.shortcuts import render, redirect, HttpResponse
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
    return render(request, 'add-menu-item.html', context)

## ---------- CRUD MENU ITEMS ---------- ##

## Add Menu Item
def add_item(request): 
    if request.method == ("POST" or "FILES"):
        Item.objects.create(
            item_name=request.POST['item_name'], 
            item_desc=request.POST['item_desc'], 
            item_price=request.POST['item_price'], 
            item_image=request.FILES['item_image'], 
            min_calories=request.POST['min_calories'],
            max_calories=request.POST['max_calories'],
            # dietary=request.POST['dietary'],
            is_available=request.POST['is_available'],
            # item_category=Category.objects.get(id=request.session['id']),
            # item_subcategory=SubCategory.objects.get(id=request.session['id']),
            # locations=Location.objects.get(id=request.session['id']),
        ) 
    # print(request.POST)   
    return redirect('/')
    # else: 
    #     pass
    #     return render(request, 'index.html')

## Fake data to get category and subcategory to 
def fakeData(request):
    Category.objects.create(category_name="Drinks")
    cate = Category.objects.get(category_name="Drinks")
    SubCategory.objects.create(subcategory_name="Bar", category=cate)
    SubCategory.objects.create(subcategory_name="Soda", category=cate)
    SubCategory.objects.create(subcategory_name="Wine", category=cate)
    return HttpResponse('Fake Data Added')

## Edit Menu Item 
# def edit(request, id):
    # context = {
    #     'item': Items.objects.get(id=id)
    # }
    # return render(request, 'edit-menu-item.html', context)


## Update Menu Items (after editing)
# def update(request, id):
#     if request.method == 'POST': 
#         update_item = Item.objects.filter(id=id)
#         if len(update_item) != 1:
#             return redirect('/') ## NEEDS TO BE UPDATED -- redirect to menu dashbaord
#         update_item[0].item_name = request.POST['item_name']
#         update_item[0].item_desc = request.POST['item_desc']
#         update_item[0].item_price = request.POST['item_price']
#         update_item[0].item_image = request.POST['item_image'] ##need to review, may need to be request.FILE 
#         update_item[0].min_calories = request.POST['min_calories']
#         update_item[0].max_calories = request.POST['max_calories']
#         update_item[0].dietary = request.POST['dietary']
#         update_item[0].is_available = request.POST['is_available']
#         update_item[0].category = request.POST['category']
#         update_item[0].subcategory = request.POST['subcategory']
#         update_item[0].save()
#     return redirect('/') ## NEEDS TO BE UPDATED -- redirect to menu dashbaord

## Delete Menu Items 
# def destroy(request, id):
#     Item.objects.get(id=id).delete()
#     return redirect('/') ## NEEDS TO BE UPDATED -- redirect to menu dashbaord

## View Menu (all items)
def view_items(request):
    context = {
        "all_items": Item.objects.all()
        }
    return render(request, 'all-menu-items.html', context)


## ---------- UPLOAD IMAGE ---------- ##

# Upload Image 
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