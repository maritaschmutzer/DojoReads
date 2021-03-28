from django.urls import path     
from . import views
urlpatterns = [
    path('', views.index),
    path('register',views.register), 	  
    path('login',views.login),
    path('books',views.show_books),
    path('books/add',views.add_books),
    path('books/<book_id>', views.add_review),
    path('users/<user_id>', views.show_user),
    path('logout', views.logout),
]