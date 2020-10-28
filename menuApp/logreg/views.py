from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.views.generic import View
from django.views.decorators.http import require_http_methods
from .decorators import my_user_passes_test, my_login_required
from logreg.models import User, Group, Permission
from adminPanel.models import Location, LocationHour, Item, ItemOption, Category, SubCategory, ItemOption
from onlineOrder.models import OnlineOrder, OrderItem
from pointOfSale.models import Order, OrderType, OrderHistory, Bill
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
    return redirect('/login/populate-data')

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
    User.objects.all().delete()
    Group.objects.all().delete()
    Location.objects.all().delete()
    LocationHour.objects.all().delete()
    Category.objects.all().delete()
    SubCategory.objects.all().delete()
    OnlineOrder.objects.all().delete()
    OrderItem.objects.all().delete()
    print("kill time")
    return redirect('/login/')

def fakeData(request):
    Location.objects.create(location_name="Main Plaza", address1='123 Way', city='New York', state='New York', country='USA', phone='+1 (555) 555-1234', is_restaurant=1, post_code='10032')
    Location.objects.create(location_name="Times Square", address1='123 Way', city='New York', state='New York', country='USA', phone='+1 (555) 555-1234', is_restaurant=1, post_code='10032')
    Location.objects.create(location_name="The Shore", address1='123 Way', city='Shore', state='New Jersey', country='USA', phone='+1 (555) 555-1234', is_restaurant=1, post_code='10032')
    LocationHour.objects.create(day_of_week='monday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="Main Plaza"))
    LocationHour.objects.create(day_of_week='monday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="Times Square"))
    LocationHour.objects.create(day_of_week='monday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="The Shore"))
    LocationHour.objects.create(day_of_week='tuesday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="Main Plaza"))
    LocationHour.objects.create(day_of_week='tuesday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="Times Square"))
    LocationHour.objects.create(day_of_week='tuesday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="The Shore"))
    LocationHour.objects.create(day_of_week='wednesday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="Main Plaza"))
    LocationHour.objects.create(day_of_week='wednesday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="Times Square"))
    LocationHour.objects.create(day_of_week='wednesday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="The Shore"))
    LocationHour.objects.create(day_of_week='thursday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="Main Plaza"))
    LocationHour.objects.create(day_of_week='thursday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="Times Square"))
    LocationHour.objects.create(day_of_week='thursday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="The Shore"))
    LocationHour.objects.create(day_of_week='friday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="Main Plaza"))
    LocationHour.objects.create(day_of_week='friday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="Times Square"))
    LocationHour.objects.create(day_of_week='friday', open_time="06:00 AM", close_time="05:00 PM", location=Location.objects.get(location_name="The Shore"))
    Category.objects.create(category_name="Lunch")
    Category.objects.create(category_name="Dinner")
    Category.objects.create(category_name="Bar")
    SubCategory.objects.create(subcategory_name="Salads", category=Category.objects.get(category_name="Lunch"))
    SubCategory.objects.create(subcategory_name="Soups", category=Category.objects.get(category_name="Lunch"))
    SubCategory.objects.create(subcategory_name="Entrees", category=Category.objects.get(category_name="Lunch"))
    SubCategory.objects.create(subcategory_name="Appetizers", category=Category.objects.get(category_name="Dinner"))
    SubCategory.objects.create(subcategory_name="Entrees", category=Category.objects.get(category_name="Dinner"))
    SubCategory.objects.create(subcategory_name="Desserts", category=Category.objects.get(category_name="Dinner"))
    SubCategory.objects.create(subcategory_name="Wine", category=Category.objects.get(category_name="Bar"))
    SubCategory.objects.create(subcategory_name="Beer", category=Category.objects.get(category_name="Bar"))
    SubCategory.objects.create(subcategory_name="Liquor", category=Category.objects.get(category_name="Bar"))
    SubCategory.objects.create(subcategory_name="Mixed", category=Category.objects.get(category_name="Bar"))
    Item.objects.create(item_name="Creature Comfort's Tropicalia", item_desc="India Pale Ale", item_price="5.00", min_calories="300", max_calories="300", dietary="N/A", is_available=1, category=Category.objects.get(category_name="Bar"), subcategory=SubCategory.objects.get(subcategory_name="Beer", category=Category.objects.get(category_name="Bar")))
    Item.objects.create(item_name="Creature Comfort's Athena", item_desc="Berliner Weisse", item_price="5.00", min_calories="300", max_calories="300", dietary="N/A", is_available=1, category=Category.objects.get(category_name="Bar"), subcategory=SubCategory.objects.get(subcategory_name="Beer", category=Category.objects.get(category_name="Bar")))
    Item.objects.create(item_name="Creature Comfort's Classic City Lager", item_desc="Good Cold Beer", item_price="4.00", min_calories="300", max_calories="300", dietary="N/A", is_available=1, category=Category.objects.get(category_name="Bar"), subcategory=SubCategory.objects.get(subcategory_name="Beer", category=Category.objects.get(category_name="Bar")))
    Item.objects.create(item_name="Creature Comfort's Automatic", item_desc="Pale Ale", item_price="4.00", min_calories="300", max_calories="300", dietary="N/A", is_available=1, category=Category.objects.get(category_name="Bar"), subcategory=SubCategory.objects.get(subcategory_name="Beer", category=Category.objects.get(category_name="Bar")))
    Item.objects.create(item_name="Creature Comfort's Bibo", item_desc="Pilsner", item_price="5.00", min_calories="300", max_calories="300", dietary="N/A", is_available=0, category=Category.objects.get(category_name="Bar"), subcategory=SubCategory.objects.get(subcategory_name="Beer", category=Category.objects.get(category_name="Bar")))
    Item.objects.create(item_name="Creature Comfort's Reclaimed Rye", item_desc="Amber Ale Aged on French Oak", item_price="6.00", min_calories="300", max_calories="300", dietary="N/A", is_available=1, category=Category.objects.get(category_name="Bar"), subcategory=SubCategory.objects.get(subcategory_name="Beer", category=Category.objects.get(category_name="Bar")))
    Item.objects.create(item_name="Burger", item_desc="It's real beef and tasty", item_price="10.00", min_calories="800", max_calories="1200", dietary="N/A", is_available=1, category=Category.objects.get(category_name="Lunch"), subcategory=SubCategory.objects.get(subcategory_name="Entrees", category=Category.objects.get(category_name="Lunch")))
    Item.objects.create(item_name="Chicken Fingers", item_desc="They're raised right, yadda, yadda", item_price="9.00", min_calories="600", max_calories="1200", dietary="N/A", is_available=1, category=Category.objects.get(category_name="Lunch"), subcategory=SubCategory.objects.get(subcategory_name="Entrees", category=Category.objects.get(category_name="Lunch")))
    Item.objects.create(item_name="Soysage", item_desc="This is if you have an aversion to dead animals", item_price="10.00", min_calories="700", max_calories="900", dietary="Vegan Friendly", is_available=1, category=Category.objects.get(category_name="Lunch"), subcategory=SubCategory.objects.get(subcategory_name="Entrees", category=Category.objects.get(category_name="Lunch")))
    Item.objects.create(item_name="Spicy Thai Chicken", item_desc="Spicy jalapeno bacon ipsum dolor amet frankfurter swine anim pancetta proident. Tail ut aute consequat sirloin excepteur aliqua pastrami voluptate.", item_price="13.00", min_calories="700", max_calories="900", dietary="Very Hot", is_available=1, category=Category.objects.get(category_name="Dinner"), subcategory=SubCategory.objects.get(subcategory_name="Entrees", category=Category.objects.get(category_name="Dinner")))
    Item.objects.create(item_name="Sweet and Sour Beef Soup", item_desc="Tongue officia turkey ut, pariatur pork belly cillum.", item_price="11.00", min_calories="700", max_calories="900", dietary="N/A", is_available=1, category=Category.objects.get(category_name="Dinner"), subcategory=SubCategory.objects.get(subcategory_name="Entrees", category=Category.objects.get(category_name="Dinner")))
    Item.objects.create(item_name="Beef Stew", item_desc="Aliquip picanha bacon cillum, tail beef duis. Boudin ham hock ex beef consectetur officia.", item_price="13.00", min_calories="700", max_calories="900", dietary="N/A", is_available=1, category=Category.objects.get(category_name="Dinner"), subcategory=SubCategory.objects.get(subcategory_name="Entrees", category=Category.objects.get(category_name="Dinner")))
    Item.objects.create(item_name="Belini", item_desc="Liquor ipsum dolor sit amet odio kensington court special snowball mint julep condimentum, lectus.", item_price="10.00", min_calories="300", max_calories="300", dietary="N/A", is_available=1, category=Category.objects.get(category_name="Bar"), subcategory=SubCategory.objects.get(subcategory_name="Mixed", category=Category.objects.get(category_name="Bar")))
    Item.objects.create(item_name="Bloody Mary", item_desc="Tellus, cutty sark scots whisky vitae tortor ketel one yorsh, ornare kir salty dog accumsan aenean chopin white horse.", item_price="15.00", min_calories="300", max_calories="300", dietary="N/A", is_available=1, category=Category.objects.get(category_name="Bar"), subcategory=SubCategory.objects.get(subcategory_name="Mixed", category=Category.objects.get(category_name="Bar")))
    Item.objects.create(item_name="Black Russian", item_desc="Bowmore, netus colorado bulldog hendrerit ultrices; salty dog interdum caribou lou.", item_price="12.00", min_calories="300", max_calories="300", dietary="N/A", is_available=1, category=Category.objects.get(category_name="Bar"), subcategory=SubCategory.objects.get(subcategory_name="Mixed", category=Category.objects.get(category_name="Bar")))
    Item.objects.create(item_name="God Mother", item_desc="Cursus gibson mattis rutrum french 75 himenaeos painkiller presbyterian jameson; cras bengal.", item_price="18.00", min_calories="300", max_calories="300", dietary="N/A", is_available=1, category=Category.objects.get(category_name="Bar"), subcategory=SubCategory.objects.get(subcategory_name="Mixed", category=Category.objects.get(category_name="Bar")))
    Item.objects.get(item_name="Soysage").locations.add(Location.objects.get(location_name="Main Plaza"))
    Item.objects.get(item_name="Soysage").locations.add(Location.objects.get(location_name="Times Square"))
    Item.objects.get(item_name="Soysage").locations.add(Location.objects.get(location_name="The Shore"))
    Item.objects.get(item_name="Burger").locations.add(Location.objects.get(location_name="Main Plaza"))
    Item.objects.get(item_name="Burger").locations.add(Location.objects.get(location_name="Times Square"))
    Item.objects.get(item_name="Burger").locations.add(Location.objects.get(location_name="The Shore"))
    Item.objects.get(item_name="Chicken Fingers").locations.add(Location.objects.get(location_name="Main Plaza"))
    Item.objects.get(item_name="Chicken Fingers").locations.add(Location.objects.get(location_name="Times Square"))
    Item.objects.get(item_name="Chicken Fingers").locations.add(Location.objects.get(location_name="The Shore"))
    return redirect('/menu-admin/')