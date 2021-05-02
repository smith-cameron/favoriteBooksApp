from django.urls import path
from . import views
urlpatterns = [
    path('', views.root),
    path('reg', views.register),
    path('login', views.login),
    path('home', views.home),
    path('addBook', views.addBook),
    path('like_book/<int:book_id>', views.like_book),
    path('unlike_book/<int:book_id>', views.unlike_book),
    path('bookDetails/<int:book_id>', views.bookDetails),
    path('unlike_book_detail/<int:book_id>', views.unlike_book_detail),
    path('like_book_detail/<int:book_id>', views.like_book_detail),
    path('editBook/<int:book_id>', views.editBook),
    path('delete/<int:book_id>', views.delete),
    path('logOut', views.logOut),
]