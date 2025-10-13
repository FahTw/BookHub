import re
from urllib import request

from django.shortcuts import render, redirect
from django.views import View

from .models import *
from django.db.models import *
from django.db.models.functions import *
from book.forms import *
from django.db import transaction
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import logout, login
from django.contrib.auth.mixins import LoginRequiredMixin

class HomeView(View, LoginRequiredMixin):
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
        return render(request,'login/login.html', {"form":form})
class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'login/register.html', {'form': form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.email
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
        else:
            print(form.errors)
        return render(request, 'login/register.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login')

class ProfileView(View, LoginRequiredMixin):
    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, 'home/profile.html', {'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()  # บันทึกลง database จริง
            return redirect('/profile')
        else:
            print(form.errors)  # ดูว่ามีปัญหาอะไร
        return render(request, 'home/profile.html', {'form': form})

class BookListView(View, LoginRequiredMixin):
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'home/book_list.html', {'books': books})

class BookDetailView(View, LoginRequiredMixin):
    def get(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        reviews = Review.objects.filter(book=book).order_by('-created_date')
        form = ReviewForm()
        return render(request, 'home/book_detail.html', {
            'book': book,
            'reviews': reviews,
            'form': form
        })

    def post(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        form = ReviewForm(request.POST)
        reviews = Review.objects.filter(book=book).order_by('-created_date')
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', book_id=book_id)

        return render(request, 'home/book_detail.html', {
            'book': book,
            'reviews': reviews,
            'form': form
        })
class CategoryView(View):
    def get(self, request, category_id):
        category = BookCategory.objects.get(id=category_id)
        books = Book.objects.filter(category=category)
        categories = BookCategory.objects.all()
        return render(request, 'home.html', {'category': category, 'books': books})

# class ReviewView(View):
#     def get(self, request, book_id):
#         form = ReviewForm()
#         book = Book.objects.get(pk=book_id)
#         reviews = Review.objects.filter(book=book)
#         return render(request, 'home/book_detail.html', {'form': form, "book": book, "reviews": reviews})
#     def post(self, request, book_id):
#         form = ReviewForm(request.POST)
#         book = Book.objects.get(pk=book_id)
#         reviews = Review.objects.filter(book=book)
#         if form.is_valid():
#             review = form.save(commit=False)
#             review.book = book
#             review.user = request.user
#             review.save()
#             return redirect('book_detail', book_id=book_id)

#         return render(request, 'home/book_detail.html', {'form': form, 'book': book, 'reviews': reviews})

class CartView(View):

    def get(self, request, user):
        cart = Cart.objects.get(id=user)
        cart_details = Cart.objects.filter(cart=cart)

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
        order_details = Order.objects.filter(order=order)

        context = {
            "order": order,
            "order_details": order_details,
        }
        return render(request, "orderhistorydetail.html", context)

class ManageBookView(View, LoginRequiredMixin):
    def get(self, request):
        form = BookForm()
        books = Book.objects.all()
        return render(request, 'owner/book_manage.html', {'form': form, 'books': books})
    def post(self, request):
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('manage_book')
        books = Book.objects.all()
        return render(request, 'owner/book_manage.html', {'form': form, 'books': books})
    def delete(self, request, book_id):
        book = Book.objects.get(id=book_id)
        book.delete()
        return redirect('manage_book')
