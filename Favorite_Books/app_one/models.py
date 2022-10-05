from django.db import models
from django.contrib import messages
import re

class UserManager(models.Manager):
    def validate(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        if len(postData["first-name"]) < 2:
            errors["first-name"] = "First Name should be minimum 2 characters"
        if len(postData["last-name"]) < 2:
            errors["last-name"] = "Last Name should be minimum 2 characters"
        if len(postData["password"]) < 8:
            errors["password"] = "Password should be 8 characters minimum"
        if postData["password"] != postData["pass-confirm"] and postData["pass-confirm"] != 0:
            errors["checkpassword"] = "Password should match!"
        if not EMAIL_REGEX.match(postData["email"]):
            errors["email"] = "Invalid email address"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.CharField(max_length=45)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)   
    objects = UserManager()

class BookManager(models.Manager):
    def validate(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors["title"] = "Title is required"
        if len(postData['description']) < 5:
            errors["description"] = "Description must be at least 2 characters"
        return errors

class Book(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(default="")
    uploaded_by = models.ForeignKey(User, related_name='uploaded_by',on_delete = models.CASCADE,default="")
    users_who_like = models.ManyToManyField(User, related_name="liked_books")
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    objects = BookManager()