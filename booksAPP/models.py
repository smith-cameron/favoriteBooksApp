from django.db import models
from datetime import datetime
import re
import bcrypt

class UserManager(models.Manager):
    def reg_validations(self, postData):
        valid_email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if postData['firstname'] == '':
            errors['firstname'] = 'First Name is required'
        elif len(postData['firstname']) < 2:
            errors['firstname'] = "First name must be at leased 2 characters."
        if postData['lastname'] == '':
            errors['lastname'] = 'Last Name is required'
        elif len(postData['lastname']) < 2:
            errors['lastname'] = "Last name must be at leased 2 characters."
        if postData['password'] == '':
            errors['password'] = 'Password is required'
        elif len(postData['password']) < 8:
            errors['password'] = "Password must be at leased 8 characters."
        if postData['email'] == '':
            errors['email'] = 'Email is required'
        elif not valid_email_check.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if postData['confirmpw'] == '':
            errors['confirmpw'] = 'Password confirmation is required'
        elif len(postData['confirmpw']) < 8:
            errors['confirmpw'] = "Password must be at leased 8 characters."
        if postData['password'] != postData['confirmpw']:
            errors['password'] = "Passwords do not match."
        if postData['dob'] == '':
            errors['dob'] = 'Date of birth is required'
        elif datetime.strptime(postData['dob'], '%Y-%m-%d') > datetime.now():
            errors['dob'] = 'Date of birth should be before todays date'
        return errors

    def login_validations(self, postData):
        valid_email_check = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if not valid_email_check.match(postData['emaillogin']):
            errors['emaillogin'] = ("Invalid email address!")
        if len(postData['passwordlogin']) < 8:
            errors['passwordlogin'] = "Password must be at leased 8 characters."
        return errors

class BookManager(models.Manager):
    def validations(self, postData):
        errors = {}
        if postData['title'] == '':
            errors['title'] = "Title is required."
        if len(postData['desc']) < 5:
            errors['desc'] = "Description must be at leased 5 characters."
        return errors


class User(models.Model):
    first_name = models.CharField(max_length = 255)
    last_name = models.CharField(max_length = 255)
    date_of_birth = models.DateTimeField()
    email = models.EmailField(max_length = 254)
    password = models.CharField(max_length = 255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = UserManager()
    # def __repr__(self):
        # return f"{self.first_name}{self.last_name}"

class Book(models.Model):
    title = models.CharField(max_length = 255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name = 'books_uploaded', on_delete = models.CASCADE)
    users_who_like = models.ManyToManyField(User, related_name ='liked_books')
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)
    objects = BookManager()
    # def __repr__(self):
        # return f"{self.title}"