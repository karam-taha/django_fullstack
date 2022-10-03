from django.db import models
import re

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        if len(postData["first-name"]) < 2:
            errors["first-name"] = "First Name should be minimum 2 characters"
        if len(postData["last-name"]) < 2:
            errors["last-name"] = "Last Name should be minimum 2 characters"
        if len(postData["password"]) < 8:
            errors["password"] = "Password should be 8 characters minimum"
        if postData["password"] != postData["pass-confirm"] and postData["pass-confirm"] != 0:
            errors["password"] = "Password should match!"
        if not EMAIL_REGEX.match(postData["email"]):
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
