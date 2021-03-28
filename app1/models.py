from __future__ import unicode_literals
from django.db import models
import bcrypt
import datetime


class BlogManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # agregue claves y valores al diccionario de errores para cada campo no válido
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First Name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last Name should be at least 2 characters"
        if len(postData['password']) < 8:
            errors["password"] = "Password should be at least 8 characters"
        if postData["password"] == postData["password_confirm"]:
            pass
        else:
            errors["password_confirm"] = "Las contraseñas deben coincidir"
        todos_los_usuarios = User.objects.all() 
        for user in todos_los_usuarios:
            if postData['email'] != user.email:
                pass
            else:
                errors["email"] = "Email ya existe"
        return errors

    def basic_validator2(self, postData):
        errors = {}
        if len(postData['title']) < 1:
            errors["title"] = "No Title"
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email= models.EmailField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()

class Author(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(Author, related_name="books", on_delete = models.CASCADE)
    uploaded_by = models.ForeignKey(User, related_name="books_uploaded", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()

class Review(models.Model):
    description = models.TextField(default="")
    rating =  models.IntegerField()
    book = models.ForeignKey(Book, related_name="reviews", on_delete = models.CASCADE)
    user = models.ForeignKey(User, related_name="reviews", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)