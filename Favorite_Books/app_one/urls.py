from django.urls import path
from . import views

urlpatterns = [
    path('',views.index),
    path('register',views.register),
    path('login',views.login),
    path('books',views.books),
    path('add_book',views.add_book),
    path('books/<int:book_id>',views.book_details),
    path('books/<int:book_id>/favorite', views.add_favorite),
    path('books/<int:book_id>/edit', views.edit_book),
    path('books/<int:book_id>/unfavorite', views.unfavorite),
    path('books/<int:book_id>/delete', views.delete_book),
    path('logout',views.logout),
]
