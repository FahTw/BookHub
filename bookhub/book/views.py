import re
from urllib import request

from django.shortcuts import render, redirect
from django.views import View

from .models import *
from django.db.models import *
from django.db.models.functions import *
from book.forms import *
from django.forms import modelformset_factory
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
            if user.is_staff:
                return redirect('/dashboard')
            else:
                return redirect('/home')
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
            return redirect('/book_detail', book_id=book_id)

        return render(request, 'home/book_detail.html', {
            'book': book,
            'reviews': reviews,
            'form': form
        })
class CategoryView(View):
    def get(self, request, category_id):
        category = BookCategory.objects.get(pk=category_id)
        books = Book.objects.filter(categories=category)
        categories = BookCategory.objects.all()
        return render(request, 'home/category.html', {'category': category, 'books': books, 'categories': categories})

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
        try:
            user = CustomUser.objects.get(id=user)
            cart = Cart.objects.filter(user=user, status='in_cart').select_related('book')
            CartFormSet = modelformset_factory(Cart, form=CartForm, extra=0)  # Pass the class, not an instance
            cartform = CartFormSet(queryset=cart)

            # Calculate totals
            total_amount = sum(item.total_price for item in cart)
            total_items = sum(item.quantity for item in cart)

            context = {
                "user": user,
                "cartform": cartform,
                "total_amount": total_amount,
                "total_items": total_items,
            }
            return render(request, "payment/cart.html", context)
        except CustomUser.DoesNotExist:
            return redirect('login')

    def post(self, request, user):
        try:
            user_obj = CustomUser.objects.get(id=user)
            form = CartForm(request.POST)
            if form.is_valid():
                cart_item = form.save(commit=False)
                cart_item.user = user_obj
                cart_item.total_price = cart_item.price * cart_item.quantity
                cart_item.save()
                return redirect('cart', user=user)
            
            cart_items = Cart.objects.filter(user=user_obj, status='in_cart').select_related('book')
            total_amount = sum(item.total_price for item in cart_items)
            total_items = sum(item.quantity for item in cart_items)
            
            context = {
                "cart_items": cart_items,
                "user_obj": user_obj,
                "total_amount": total_amount,
                "total_items": total_items,
                "cart_form": form,
            }
            return render(request, "payment/cart.html", context)
        except CustomUser.DoesNotExist:
            return redirect('login')

class PaymentView(View):
    def get(self, request, user):
        try:
            user_obj = CustomUser.objects.get(id=user)
            # Get user's latest order or create new one from cart
            latest_order = Order.objects.filter(user=user_obj).order_by('-order_date').first()
            
            context = {
                "order": latest_order,
                "user_obj": user_obj,
                "payment_form": PaymentForm(),
            }
            return render(request, "payment/payment.html", context)
        except CustomUser.DoesNotExist:
            return redirect('login')
    
    def post(self, request, user):
        try:
            user_obj = CustomUser.objects.get(id=user)
            form = PaymentForm(request.POST, request.FILES)
            if form.is_valid():
                payment = form.save(commit=False)
                payment.save()
                return redirect('order_history_user', user=user)
            
            latest_order = Order.objects.filter(user=user_obj).order_by('-order_date').first()
            context = {
                "order": latest_order,
                "user_obj": user_obj,
                "payment_form": form,
            }
            return render(request, "payment/payment.html", context)
        except CustomUser.DoesNotExist:
            return redirect('login')

class OrderHistoryView(View):
    def get(self, request, user):
        try:
            user_obj = CustomUser.objects.get(id=user)
            orders = Order.objects.filter(user=user_obj).order_by("-order_date").select_related('cart', 'cart__book')
            
            context = {
                "orders": orders,
                "user_obj": user_obj,
            }
            return render(request, "orderhistory.html", context)
        except CustomUser.DoesNotExist:
            return redirect('login')

class OrderHistoryDetailView(View):
    def get(self, request, user, order):
        try:
            user_obj = CustomUser.objects.get(id=user)
            order_obj = Order.objects.get(id=order, user=user_obj)
            
            # Get cart details for this order
            cart_info = order_obj.cart
            
            context = {
                "order": order_obj,
                "cart_info": cart_info,
                "user_obj": user_obj,
            }
            return render(request, "orderhistorydetail.html", context)
        except (CustomUser.DoesNotExist, Order.DoesNotExist):
            return redirect('login')

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
