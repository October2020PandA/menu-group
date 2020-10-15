from django.db import models
import string
import bcrypt
import re

# Create your models here.
class UserManager(models.Manager):
    def user_validator(self, postData):
        errors = {}
        email_regex = re.compile(r'^([a-zA-Z0-9_\-\.]+)@([a-zA-Z0-9_\-\.]+)\.([a-zA-Z]{2,5})$')
        existing_email = User.objects.filter(email=postData['email_address'])
        if len(postData['first_name']) < 2 or postData['first_name'].isdigit():
            errors['first_name'] = 'First name must be at least 2 characters long and/or contain no numbers'
        if len(postData['last_name']) < 2 or postData['last_name'].isdigit():
            errors['last_name'] = 'Last name must be at least 2 characters long and/or contain no numbers'
        if not email_regex.match(postData['email_address']):
            errors['email_address'] = 'Invalid email address'
        elif len(existing_email) != 0:
            errors['email_address'] = 'Email address already linked to a user'
        if len(postData['pw']) < 8 :
            errors['pw_len'] = 'Password must be at least 8 digits long'
        if postData['pw'].isdigit() and postData['pw'].isalpha():
            errors['pw_alpha'] = 'Password must contain at least one number and one character'
        if postData['pw'] != postData['pw_confirm']:
            errors['pw_confirm'] = 'Passwords do not match'
        return errors
    def login_validator(self, postData):
        errors = {}
        existing_email = User.objects.filter(email=postData['email_address_lg'])
        if len(existing_email) == 0:
            errors['lg_email_address'] = 'Invalid username'
        elif not bcrypt.checkpw(postData['pw_lg'].encode(), existing_email[0].pw.encode()):
            errors['lg_pw'] = 'Invalid username and/or password'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=50, blank=True)
    pw = models.CharField(max_length=255)
    last_login = models.DateTimeField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Group(models.Model):
    group_name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='groups', related_query_name='groups')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Permission(models.Model):
    permission_name = models.CharField(max_length=255)
    users = models.ManyToManyField(User, related_name='permissions', related_query_name='permissions')
    groups = models.ManyToManyField(Group, related_name='permissions', related_query_name='permissions')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)