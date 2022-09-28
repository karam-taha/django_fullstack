from django.shortcuts import render,redirect
from django.contrib import messages
from .models import *

def index(request):
    return redirect('/shows')

def shows(request):
    context={
        'shows': Show.objects.all()
    }
    return render(request,'shows.html',context)

def new_show(request):
    return render(request,'new_show.html')

def create_show(request):
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/shows/new')
    Show.objects.create(title=request.POST['title'], network=request.POST['network'],
    desc=request.POST['desc'],released_at=request.POST['release'])
    return redirect('/shows/new')

def show_id(request,id):
    show = Show.objects.get(id=id)
    context = {
        "show": show,
    }
    return render(request,'show_info.html',context)

def edit_show(request,id):
    show = Show.objects.get(id=id)
    context = {
        "show": show,
        "date": str(Show.objects.get(id=id).released_at)
    }
    return render(request,'edit_show.html',context)

def update_show(request,id):
    errors = Show.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/shows/new')
    selected = Show.objects.get(id=id)
    if request.POST['title']:
        selected.title = request.POST['title']
    
    if request.POST['network']:
        selected.network = request.POST['network']
    
    if request.POST['release']:
        selected.released_at = request.POST['release']
    
    if request.POST['desc']:
        selected.desc = request.POST['desc']
    selected.save()
    return redirect('/shows')

def destroy_show(request, id):
    Show.objects.get(id=id).delete()
    return redirect("/shows")