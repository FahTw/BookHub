import re

from django.shortcuts import render, redirect
from django.views import View
from .models import *
from django.db.models import *
from django.db.models.functions import *
from book.forms import *
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login

class HomeView(View):
    def get(self, request):
        categories = BookCategory.objects.all()
        return render(request, 'home/home.html', {'categories': categories})

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login/login.html', {"form": form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request,user)
            return redirect('/book/')
        else:
            print(form.errors)
        return render(request,'home/home.html', {"form":form})
class RegisterView(View):
    
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'login/register.html', {'form': form})
    
    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            # save in db
            user = form.save(commit=False)
            user.username = user.email
            user.set_password(form.cleaned_data['password'])
            user.save()
            return redirect('/login/')
        else:
            print(form.errors)
        return render(request, 'login/login.html', {'form': form})

class ProfileView(View):
    def get(self, request):
        form = ProfileForm()
        return render(request, 'profile.html')
    def post(self, request):
        # Handle profile update logic here
        form = ProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('/book/')
        return redirect('profile')

class BookListView(View):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'book_list.html', {'books': books})

class CategoryView(View):
    def get(self, request, category_id):
        category = BookCategory.objects.get(id=category_id)
        books = Book.objects.filter(category=category)
        categories = BookCategory.objects.all()
        return render(request, 'home.html', {'category': category, 'books': books})

class ReviewView(View):
    def get(self, request, book_id):
        form = ReviewForm()
        book = Book.objects.get(pk=book_id)
        return render(request, 'review.html', {'form': form, 'book': book})
    def post(self, request, book_id):
        form = ReviewForm(request.POST)
        book = Book.objects.get(pk=book_id)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', book_id=book_id)
        

        return render(request, 'review.html', {'form': form, 'book': book})

class CartView(View):

    def get(self, request, user):
        cart = Cart.objects.get(id=user)
        cart_details = CartDetail.objects.filter(cart=cart)

        context = {
            "cart": cart,
            "cart_details": cart_details,
        }
        return render(request, "cart.html", context)

class PaymentView(View):

    def get(self, request, user):
        order = Order.objects.get(id=user)
        context = {
            "order": order,
        }
        return render(request, "payment.html", context)

class OrderHistoryView(View):

    def get(self, request, user):
        orders = Order.objects.filter(user=user).order_by("-order_date")
        context = {
            "orders": orders,
        }
        return render(request, "orderhistory.html", context)

class OrderHistoryDetailView(View):

    def get(self, request, user, order):
        order = Order.objects.get(id=order, user=user)
        order_details = OrderDetail.objects.filter(order=order)

        context = {
            "order": order,
            "order_details": order_details,
        }
        return render(request, "orderhistorydetail.html", context)

class ManageBookView(View):
    def get(self, request):
        form = ManageBookForm()
        books = Book.objects.all()
        return render(request, 'book_manage.html', {'form': form, 'books': books})
    def post(self, request):
        form = ManageBookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_book')
        books = Book.objects.all()
        return render(request, 'book_manage.html', {'form': form, 'books': books})
