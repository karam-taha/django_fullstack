from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from .models import User,Message,Comment
import bcrypt

def index(request):
    if 'id' in request.session.keys():
        return redirect('/wall')
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
            return redirect('/wall')
        else:
            messages.error(request,'Invalid password.')
            return redirect('/')

def wall(request):
    context = {
        'user':User.objects.get(id=request.session['id']),
        'post_data':Message.objects.all(),
        'comment_data':Comment.objects.all(),
    }
    return render(request, 'wall.html',context)

def add_message(request):
    Message.objects.create(message=request.POST['add_message'], user=User.objects.get(id=request.session['id']))
    messages.success(request,'Message posted successfully.')
    return redirect('/wall')

def delete_message(request,id):
    m = Message.objects.get(id=id)
    m.delete()
    return redirect('/wall')    

def comment(request):
    Comment.objects.create(comment=request.POST['comment'],user=User.objects.get(id=request.session['id']),message=Message.objects.get(id=request.POST['message_ID']) )
    return redirect('/wall')    


def logout(request):
    request.session.clear()
    return redirect('/')