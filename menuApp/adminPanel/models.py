from django.db import models

# Create your models here.
class Location(models.Model):
    location_name = models.CharField(max_length=255)
    address1 = models.CharField(max_length=255)
    address2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=255)
    state = models.CharField(max_length=100)   
    county = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=3, blank=True)
    is_restaurant = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Category(models.Model):
    category_name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class SubCategory(models.Model):
    subcategory_name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, related_name='subcategories', related_query_name='subcategories', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Item(models.Model):
    item_name = models.CharField(max_length=255)
    item_desc = models.TextField()
    item_price = models.DecimalField(max_digits=7, decimal_places=3)
    item_image = models.CharField(max_length=255, blank=True)
    min_calories = models.IntegerField()
    max_calories = models.IntegerField()
    dietary = models.TextField(blank=True)
    is_available = models.BooleanField()
    category = models.ForeignKey(Category, related_name='items', related_query_name='items', on_delete=models.CASCADE)
    subcategory = models.ForeignKey(SubCategory, related_name='items', related_query_name='items', on_delete=models.CASCADE)
    locations = models.ManyToManyField(Location, related_name='items', related_query_name='items')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class ItemOption(models.Model):
    option_discount = models.DecimalField(max_digits=7, decimal_places=3)
    item = models.ForeignKey(Item, related_name='options', related_query_name='options', on_delete=models.CASCADE)
    option = models.ForeignKey(Item, related_name='itemOptions', related_query_name='itemOptions', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)