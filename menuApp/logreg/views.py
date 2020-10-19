from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.views.generic import View
from django.views.decorators.http import require_http_methods
from .decorators import my_user_passes_test, my_login_required
from .models import User, Group
from adminPanel.models import Location, LocationHour
from datetime import datetime
import bcrypt

# Create your views here.

def index(request):
    if User.objects.all().count() == 0:
        return redirect('/login/register')
    context = {
        'title': 'Menu Registration',
    }
    print(request.user)
    return render(request, 'main_login.html', context)

def initialRegister(request):
    if User.objects.all().count() == 0:
        context = {
            'title': 'Menu Registration',
        }
        return render(request, 'add_initial_user.html', context)
    else: 
        return redirect('/login/')

def register(request):
    if User.objects.all().count() == 0:
        return redirect('/login/initial-register')
    context = {
        'title': 'Register as New User',
    }
    return render(request, 'add_user.html', context)

@my_login_required(login_url="/login/")
def location(request):
    context = {
        'cardHeader': 'Add Main Location',
    }
    return render(request, 'add_location.html', context)

@require_http_methods(["POST"])
@my_login_required(login_url="/login/")
def locationCreate(request):
    errors = Location.objects.location_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/login/location')
    Location.objects.create(location_name=request.POST['location_name'], address1=request.POST['address-1'], address2=request.POST['address-2'], city=request.POST['city'], state=request.POST['state_province'], country=request.POST['country'], phone=request.POST['phone_num'], is_restaurant=1)
    if request.POST['add-another'] == "repeat":
        return redirect('/login/location')
    return redirect('/login/hours')

@my_login_required(login_url="/login/")
def openHours(request):
    context = {
        'cardHeader': 'Add Restaurant Hours',
    }
    return render(request, 'add_hours.html', context)

@require_http_methods(["POST"])
@my_login_required(login_url="/login/")
def openHoursCreate(request):
    weekdays = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    for day in weekdays:
        if day in request.POST:
            openTime = day + '-open'
            closeTime = day + '-close'
            existingDay = LocationHour.objects.filter(day_of_week=day)
            locs = Location.objects.all()
            for loc in locs:
                if existingDay.count() == 0:
                    LocationHour.objects.create(day_of_week=day, open_time=request.POST[openTime], close_time=request.POST[closeTime], location=loc)
                else:
                    locHr = LocationHour.objects.get(day_of_week=day, location=loc)
                    locHr.open_time = openTime
                    locHr.close_time = closeTime
                    locHr.save()
    return redirect('/menu-admin/')

@my_login_required(login_url="/login/")
def employee(request):
    context = {
        'cardHeader': 'Add Employees',
    }
    return render(request, 'add_employee.html', context)

@require_http_methods(["POST"])
def initialCreate(request):
    errors = User.objects.user_validator(request.POST)
    if User.objects.all().count() == 0:
        initialAdmin = True
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/login/register')
    hashed_pw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],  pw=hashed_pw, middle_name=request.POST['middle_name'], phone=request.POST['phone_num'], last_login=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    request.session['login_id'] = User.objects.get(email=request.POST['email']).id
    if initialAdmin:
        Group.objects.create(group_name='Restaurant Admin')
        g = Group.objects.get(group_name='Restaurant Admin')
        u = User.objects.get(email=request.POST['email'])
        g.users.add(u)
    return redirect('/login/location')

@require_http_methods(["POST"])
def userCreate(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/login/register')
    hashed_pw = bcrypt.hashpw(request.POST['pw'].encode(), bcrypt.gensalt()).decode()
    User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'],  pw=hashed_pw, phone=request.POST['phone_num'], last_login=datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
    request.session['login_id'] = User.objects.get(email=request.POST['email']).id
    return redirect('/order-online/')

@require_http_methods(["POST"])
def authenticate(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
        return redirect('/login/')
    user = User.objects.get(email=request.POST['email'])
    request.session['login_id'] = user.id
    return redirect('/order-online/') 

def logout(request):
    if 'login_id' in request.session:
        del request.session['login_id']
    return redirect('/order-online/')

def clearDb(request):
    if User.objects.all().count() == 0:
        print("uh-oh")
    else:
        User.objects.all().delete()
        Group.objects.all().delete()
        Location.objects.all().delete()
        LocationHour.objects.all().delete()
        print("kill time")
    return redirect('/login/')

# def fakeData(request):
#     Category.objects.create(category_name="Drinks")
#     cate = Category.objects.get(category_name="Drinks")
#     SubCategory.objects.create(subcategory_name="Bar", category=cate)
#     SubCategory.objects.create(subcategory_name="Soda", category=cate)
#     SubCategory.objects.create(subcategory_name="Wine", category=cate)
#     return HttpResponse('Fake Data Added')