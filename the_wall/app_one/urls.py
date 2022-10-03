from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('wall',views.wall),
    path('logout',views.logout),
    path('add_message',views.add_message),
    path('delete_message/<int:id>',views.delete_message),
    path('comment',views.comment),
]
