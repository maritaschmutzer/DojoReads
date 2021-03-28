from django.shortcuts import render, redirect, HttpResponse
from .models import User, Book, Review, Author
from django.contrib import messages
import bcrypt

def index(request):
    context = {
        "all_the_users" : User.objects.all(),
    }
    return render(request, 'index.html', context)


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key,value in errors.items():
            messages.error(request, value, key)
        return redirect ("/")
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
        User.objects.create(
                first_name = request.POST["first_name"],
                last_name = request.POST["last_name"],
                email = request.POST["email"],
                password = pw_hash,
            )
        request.session['userid'] = User.objects.last().id
    return redirect("/books")

def login(request):
    user = User.objects.filter(email=request.POST['email'])
    if user:
        logged_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
            request.session['userid'] = logged_user.id
            return redirect('/books')
    return redirect("/")


def show_books(request):
    user = User.objects.get(id = request.session['userid'])
    context = {
        "usuario" : user,
        "last_3_books" : Book.objects.all().order_by("-created_at")[0:3],
        "all_books_3": Book.objects.all().order_by("-created_at")[3::],
        "all_the_books" : Book.objects.all(),
        "all_the_reviews" : Review.objects.all(),
        "all_the_users" : User.objects.all(),
    }
    print(len(Book.objects.all().order_by("-created_at")))
    return render(request,"index2.html", context)

def add_books(request):
    if request.method == "POST":
        errors = Book.objects.basic_validator2(request.POST)
        if len(errors) > 0:
            for key,value in errors.items():
                messages.error(request, value, key)
            return redirect ("/books/add")
        else:
            Author.objects.create(
                name = request.POST['author']
            )
            print("autor creado")
            user = User.objects.get(id = request.session['userid'])
            autor = Author.objects.last()
            Book.objects.create(
                title = request.POST["title"],
                author = autor,
                uploaded_by = user,
            )
            print("libro creado")
            Review.objects.create(
                description = request.POST['description'],
                rating = request.POST['rating'],
                book = Book.objects.last(),
                user = user,
            )
            print("review creado")
        return redirect("/books")
    else:
        user = User.objects.get(id = request.session['userid'])
        context = {
            "usuario" : user,
            "all_the_books" : Book.objects.all(),
        }
        return render(request,"index3.html", context)

def add_review(request, book_id):
    if request.method == "POST":
        Review.objects.create(
            description = request.POST['description'],
            rating = request.POST['rating'],
            book = Book.objects.get(id=book_id),
            user = User.objects.get(id = request.session['userid'])
        )
        return redirect("/books")
    else: 
        context = {
            "book" :  Book.objects.get(id = book_id),
        }
    return render(request,"index4.html", context)

def show_user(request, user_id):
    user = User.objects.get(id = user_id)
    context = {
        "user" : user,
        "len_reviews" : len(user.reviews.all())
    }
    return render(request,"index5.html",context)

def logout(request):
    logged_user = []
    request.session.clear()
    return redirect("/")