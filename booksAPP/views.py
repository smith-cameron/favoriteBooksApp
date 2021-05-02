from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def root(request):
    return render(request, 'login_reg.html')

def register(request):
    if request.method == 'POST':
        email_check = User.objects.filter(email = request.POST['email'])
        if len(email_check) > 0:
            print('regEmail error')
            messages.error(request, "Email already exists. Please log in.")
            return redirect('/')
        errors = User.objects.reg_validations(request.POST)
        if len(errors) > 0:
            print('validation error')
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            new_user = User.objects.create(
                first_name = request.POST['firstname'],
                last_name = request.POST['lastname'],
                date_of_birth = request.POST['dob'],
                email = request.POST['email'],
                password = pw_hash
            )
            request.session['currentUser'] = new_user.id
            return redirect('/home')
    return redirect('/')

def login(request):
    if request.method == 'POST':
        users = User.objects.filter(email=request.POST['emaillogin'])
        if not users:
            print('login email error')
            messages.error(request, "Email not in data base.")
            return redirect('/')
        errors = User.objects.login_validations(request.POST)
        if len(errors) > 0:
            print('login validation error')
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        if users:
            logged_user = users[0]
        if bcrypt.checkpw(request.POST['passwordlogin'].encode(), logged_user.password.encode()):
            request.session['currentUser'] = logged_user.id
            return redirect('/home')
    return redirect('/')

def home(request):
    context = {
        'user': User.objects.get(id = request.session['currentUser']),
        'allBooks': Book.objects.all(),
    }
    return render(request, 'allbooks.html', context)

def addBook(request):
    if request.method == 'POST':
        errors = Book.objects.validations(request.POST)
        print('about to go into error')
        if len(errors) > 0:
            print(len(errors))
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/home')
        else:
            newBook = Book.objects.create(
                title = request.POST['title'],
                desc = request.POST['desc'],
                uploaded_by = User.objects.get(id = request.session['currentUser'])
                )
            currentUser = User.objects.get(id = request.session['currentUser'])
            currentUser.liked_books.add(newBook)
            return redirect('/home')
    return render(request, 'allbooks.html')

def like_book(request, book_id):
    book_to_like = Book.objects.get(id = book_id)
    this_user = User.objects.get(id = request.session['currentUser'])
    this_user.liked_books.add(book_to_like)
    return redirect('/home')

def unlike_book(request, book_id):
    book_to_unlike = Book.objects.get(id = book_id)
    this_user = User.objects.get(id = request.session['currentUser'])
    this_user.liked_books.remove(book_to_unlike)
    return redirect('/home')

def unlike_book_detail(request, book_id):
    if request.method == 'POST':
        book_to_unlike = Book.objects.get(id = book_id)
        this_user = User.objects.get(id = request.session['currentUser'])
        this_user.liked_books.remove(book_to_unlike)
        return redirect(f'/bookDetails/{book_id}')
    return redirect(f'/bookDetails/{book_id}')

def like_book_detail(request, book_id):
    if request.method == 'POST':
        book_to_like = Book.objects.get(id = book_id)
        this_user = User.objects.get(id = request.session['currentUser'])
        this_user.liked_books.add(book_to_like)
        return redirect(f'/bookDetails/{book_id}')
    return redirect(f'/bookDetails/{book_id}')

def bookDetails(request, book_id):
    context = {
        'selectedBook': Book.objects.get(id = book_id),
        'user': User.objects.get(id = request.session['currentUser']),
        'allBooks': Book.objects.all(),
    }
    return render(request, 'view_book.html', context)

def editBook(request, book_id):
    selectedBook = Book.objects.get(id = book_id)
    context = {
        'selectedBook': selectedBook,
        'user': User.objects.get(id = request.session['currentUser']),
    }
    if request.method == 'POST':
        errors = Book.objects.validations(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/editBook')
        else:
            selectedBook.title = request.POST['title']
            selectedBook.desc = request.POST['desc']
            selectedBook.save()
            return redirect(f'/bookDetails/{book_id}')
    return render(request, 'edit_book.html', context)

def delete(request, book_id):
    book_to_delete = Book.objects.get(id = book_id)
    book_to_delete.delete
    return redirect('/home')

def logOut(request):
    request.session.flush()
    return redirect('/')