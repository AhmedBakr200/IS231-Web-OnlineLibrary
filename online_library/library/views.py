from django.shortcuts import get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Profile, Book, BorrowRecord
import re
from .forms import BookForm
from datetime import datetime
def home(request):
    return render(request, 'index.html')

@login_required
def borrowed_books(request):
    return render(request, 'borrowed_books.html')

@login_required
def user_books(request):
    books = Book.objects.all()
    borrowed_books = list(BorrowRecord.objects.filter(
    user=request.user,
    returned=False
    ).values_list('book_id', flat=True)
)
    context = {
        'books': books,
        'borrowed_books' : borrowed_books,
    }
    return render(request, 'user_books.html', context)

@login_required
def book_details(request, id):
    book = get_object_or_404(Book, id=id)
    borrowed = BorrowRecord.objects.filter(user=request.user, book = book, returned=False).exists()
    available = book.copies > 0
    context = {
        'book': book, 
        'borrowed':borrowed, 
        'available':available
    }
    return render(request, 'user_book_details.html', context)


@login_required
def borrow_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    already_borrowed = BorrowRecord.objects.filter(
        user=request.user,
        book=book,
        returned=False
    ).exists()

    if already_borrowed:
        return redirect(request.META.get('HTTP_REFERER', 'home'))

    if book.copies > 0:

        BorrowRecord.objects.create(
            user=request.user,
            book=book,
            returned=False
        )

        book.copies -= 1
        book.save()

    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required
def unborrow_book(request, book_id):

    book = get_object_or_404(Book, id=book_id)

    borrow_record = BorrowRecord.objects.filter(
        user=request.user,
        book=book,
        returned=False
    ).first()

    if borrow_record:

        borrow_record.returned = True
        borrow_record.save()

        book.copies += 1
        book.save()

    return redirect('books')
  
@login_required
def search(request):
    title = request.GET.get('title', '')
    author = request.GET.get('author', '')
    category = request.GET.get('category', 'Any')
    availability = request.GET.get('availability', 'Any')

    books = Book.objects.all()

    if title:
        books = books.filter(title__icontains=title)

    if author:
        books = books.filter(author__icontains=author)

    if category != 'Any':
        books = books.filter(category=category)

    if availability != 'Any':
        books = books.filter(availability=availability)

    return render(request, 'search.html', {
        'books': books,
        'title': title,
        'author': author,
        'category': category,
        'availability': availability,
    })

def signup_view(request):

    if request.method == "POST":

        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        # username exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists!")
            return redirect('signup')

        # email exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists!")
            return redirect('signup')

        # password strength
        pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$'

        if not re.match(pattern, password):

            messages.error(
            request,
            "Password must contain uppercase, lowercase, number, and be at least 8 characters!"
            )

            return redirect('signup')
        
        # password match
        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return redirect('signup')

        # create user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        Profile.objects.create(user=user)

        messages.success(request, "Account created successfully!")

        return redirect('login')

    return render(request, 'signup.html')


def login_view(request):

    if request.method == "POST":
        
        username_email = request.POST.get('username_email')
        password = request.POST.get('password')

        # check if input is email
        if '@' in username_email:

            try:
                user_obj = User.objects.get(email=username_email)
                username = user_obj.username

            except User.DoesNotExist:
                messages.error(
                    request,
                    "Invalid username/email or password!"
                )
                return redirect('login')

        else:
            username = username_email

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:
            login(request, user)
            
            messages.success(request, "Login successful!")

            next_url = request.GET.get('next')

            if next_url:
                return redirect(next_url)

            return redirect('books')

        else:
            messages.error(
                request,
                "Invalid username/email or password!"
            )
            return redirect('login')

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('login')

def admin_books(request):
    books = Book.objects.all()
    return render(request, 'admin_books.html', {'books': books})


def admin_book_details(request, id):
    book = get_object_or_404(Book, id=id)
    return render(request, 'admin_book_details.html', {'book': book})


def increase_copies(request, id):
    book = get_object_or_404(Book, id=id)
    if book.copies == 0:
        book.availability = "Available"
    book.copies += 1
    book.save()
    return redirect('admin_books')


def decrease_copies(request, id):
    book = get_object_or_404(Book, id=id)
    if book.copies > 0:
        book.copies -= 1
        if book.copies == 0:
            book.availability = 'Out of Stock'
        book.save()
    return redirect('admin_books')


def delete_book(request, id):
    book = get_object_or_404(Book, id=id)
    if request.method == 'POST':
        book.delete()
    return redirect('admin_books')


def Validate_book(new_book_data):
    errors = []
    if new_book_data['year'] > datetime.now().year:
        errors.append("The Publishing Year Can't Be In The Future.")
    
    if new_book_data['copies'] < 1:
        errors.append("The Book Copies Can't Be Less Than 1")

    return errors


def admin_add_book(request):
    form = BookForm()
    errors = []
    if request.method == 'POST':
        errors = []
        form = BookForm(request.POST)
        if form.is_valid():
            new_book_data = form.cleaned_data
            errors=Validate_book(new_book_data)
            if not errors:
                new_book = form.save()
                return redirect('admin_book_details',id = new_book.id)
    return render(request, 'admin_add_book.html',{'form':form, 'errors':errors})



def admin_edit_book(request, id):
    old_book = get_object_or_404(Book, id=id)
    errors = []
    form = BookForm(instance=old_book)
    if request.method == 'POST':
       form = BookForm(request.POST, instance=old_book)
       if form.is_valid():
            new_book_data = form.cleaned_data
            errors=Validate_book(new_book_data)
            if not errors:
                form.save()
                return redirect('admin_book_details',id = id)
    return render(request, 'admin_edit_book.html',{'form':form, 'errors':errors})
