from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    if 'id' in request.session.keys():
        return redirect('/books')
    return render(request,'index.html')

def register(request):
    errors = User.objects.validate(request.POST)
    if len(errors) > 0:
        for key, val in errors.items():
            messages.error(request, val)
        print ('Invalid input')
        return redirect('/')
    else:
        hash_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print (hash_password)
        User.objects.create(first_name=request.POST['first-name'],last_name=request.POST['last-name'],email=request.POST['email'],password=hash_password)
        user = User.objects.filter(email=request.POST['email'])
        request.session['id'] = user[0].id
    return redirect('/')

def login(request):
    email = request.POST['email']
    password = request.POST['password']
    user = User.objects.filter(email=email)
    if len(user) == 0:
        messages.error(request,"User not recognized")
        return redirect('/')
    else:
        if ( bcrypt.checkpw(password.encode(), user[0].password.encode())):
            print ('password matches')
            request.session['id'] = user[0].id
            return redirect('/books')
        else:
            messages.error(request,'Invalid password.')
            return redirect('/')

def books(request):
    context = {
        'user':User.objects.get(id=request.session['id']),
        'booklist':Book.objects.all(),
    }
    return render(request, 'books.html',context)

def add_book(request):
    errors = Book.objects.validate(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return redirect('/books')
    else:
        uploaded = User.objects.get(id=request.session['id'])
        book = Book.objects.create(
            title=request.POST['title'],
            description = request.POST['description'],
            uploaded_by = uploaded,
        )
        this_book = Book.objects.last()
        print(this_book)
        uploaded.liked_books.add(this_book)
    return redirect('/books')

def book_details(request, book_id):
    context = {
        'userid' : User.objects.get(id=request.session['id']),
        'details' : Book.objects.get(id=book_id),
        'my_faves': Book.objects.filter(users_who_like=request.session['id'])
    }
    return render (request, 'details.html', context)

def add_favorite(request, book_id):
    print("this is working")
    this_book = Book.objects.get(id= book_id)
    this_user = User.objects.get(id=request.session['id'])
    this_user.liked_books.add(this_book)
    print ("hello im here")
    return HttpResponseRedirect (request.META.get('HTTP_REFERER'))

def edit_book(request, book_id):
    errors = Book.objects.validate(request.POST)
    if len(errors)>0:
        for key, value in errors.items():
            messages.error(request,value)
        return HttpResponseRedirect (request.META.get('HTTP_REFERER'))
    else:
        book_to_update = Book.objects.get(id=book_id)
        book_to_update.title=request.POST['title']
        book_to_update.description = request.POST['description']
        book_to_update.save()
        return HttpResponseRedirect (request.META.get('HTTP_REFERER'))

def unfavorite(request, book_id):
    this_book = Book.objects.get(id= book_id)
    this_user = User.objects.get(id=request.session['id'])
    this_user.liked_books.remove(this_book)
    return HttpResponseRedirect (request.META.get('HTTP_REFERER'))

def delete_book(request, book_id):
    to_delete = Book.objects.get(id= book_id)
    to_delete.delete()
    return redirect('/books')

def logout(request):
    request.session.clear()
    return redirect('/')