from django.shortcuts import render,redirect
from django.contrib import messages
import bcrypt
from .models import *


def index(request):
    return render(request,'index.html')

def register(request):

    errors = User.objects.basic_validator(request.POST)

    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')

    first_name = request.POST.get('first-name')
    last_name = request.POST.get('last-name')
    email = request.POST.get('email')
    password = request.POST.get('password')
    pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
    new_user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=pw_hash
        )
    new_user.save()
    request.session['email'] = email
    return redirect('/success')

def login(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    user = User.objects.filter(email=email)
    request.session['email'] = email

    if user:
        if bcrypt.checkpw(password.encode(), user[0].password.encode()):
            return redirect('/success')
        else:
            return redirect('/')
    return redirect('/')

def success(request):
    if 'user' not in request.session:
        return redirect('/')
    email = request.session['email']
    user = User.objects.filter(email=email)
    context = {
        "user": user[0]
    }
    return render(request, "success.html", context)

def logout(request):
    request.session.clear()
    return redirect("/")