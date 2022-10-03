from django.db import models
from django.contrib import messages
import re

class UserManager(models.Manager):
    def validate(self, data):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        if len(data["first-name"]) < 2:
            errors["first-name"] = "First Name should be minimum 2 characters"
        if len(data["last-name"]) < 2:
            errors["last-name"] = "Last Name should be minimum 2 characters"
        if len(data["password"]) < 8:
            errors["password"] = "Password should be 8 characters minimum"
        if data["password"] != data["pass-confirm"] and data["pass-confirm"] != 0:
            errors["checkpassword"] = "Password should match!"
        if not EMAIL_REGEX.match(data["email"]):
            errors["email"] = "Invalid email address"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)   
    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    user = models.ForeignKey(User, related_name='messages',on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

class Comment(models.Model):
    comment = models.TextField()
    user = models.ForeignKey(User, related_name='u_comments',on_delete = models.CASCADE)
    message = models.ForeignKey(Message, related_name='m_comments',on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True) 
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()