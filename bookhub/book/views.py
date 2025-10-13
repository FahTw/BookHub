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
from datetime import datetime

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

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('/login')

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
        try:
            user = CustomUser.objects.get(id=user)
            cart = Cart.objects.filter(user=user, status='in_cart').select_related('book')

            # Calculate totals
            total_amount = sum(item.total_price for item in cart)
            total_items = sum(item.quantity for item in cart)

            context = {
                "user": user,
                "cart": cart,
                "total_amount": total_amount,
                "total_items": total_items,
            }
            return render(request, "payment/cart.html", context)
        except CustomUser.DoesNotExist:
            return redirect('login')

    def post(self, request, user):
        try:
            user_obj = CustomUser.objects.get(id=user)
            action = request.POST.get('action')
            cart_id = request.POST.get('cart_id')
            
            if action == 'remove' and cart_id:
                # Remove item from cart
                Cart.objects.filter(id=cart_id, user=user_obj).delete()
                return redirect('cart', user=user)
            
            elif action == 'update' and cart_id:
                # Update quantity
                quantity_change = int(request.POST.get('quantity_change', 0))
                cart_item = Cart.objects.get(id=cart_id, user=user_obj)
                new_quantity = cart_item.quantity + quantity_change
                
                if new_quantity > 0 and new_quantity <= cart_item.book.stock:
                    cart_item.quantity = new_quantity
                    cart_item.total_price = cart_item.price * cart_item.quantity
                    cart_item.save()
                
                return redirect('cart', user=user)
            
            return redirect('cart', user=user)
        except (CustomUser.DoesNotExist, Cart.DoesNotExist):
            return redirect('login')

class PaymentView(View):
    def get(self, request, user):
        try:
            user_obj = CustomUser.objects.get(id=user)
            cart_items = Cart.objects.filter(user=user_obj, status='in_cart')
            
            # Calculate total amount from cart
            total_amount = sum(item.total_price for item in cart_items)
            
            context = {
                "user_obj": user_obj,
                "cart_items": cart_items,
                "total_amount": total_amount,
            }
            return render(request, "payment/payment.html", context)
        except CustomUser.DoesNotExist:
            return redirect('login')
    
    def post(self, request, user):
        try:
            user_obj = CustomUser.objects.get(id=user)
            cart_items = Cart.objects.filter(user=user_obj, status='in_cart')
            payment_method = request.POST.get('method')

            for cart_item in cart_items:
                # Create Order for each cart item
                order = Order.objects.create(
                    user=user_obj,
                    cart=cart_item,
                    order_date=datetime.now(),
                    total_amount=cart_item.total_price,
                    status='unpaid'  # Start as unpaid, will update after payment
                )
                        
                # Create Payment for each order
                payment = Payment.objects.create(
                    order=order,
                    payment_date=datetime.now(),
                    method=payment_method,
                    amount=cart_item.total_price,
                    status='pending'
                )

                # Add payment slip if uploaded and not cash on delivery
                if payment_method != 'cash' and 'payment_slip' in request.FILES:
                    payment.payment_slip = request.FILES['payment_slip']
                    payment.save()

                # Update order status based on payment method
                if payment_method == 'cash':
                    order.status = 'unpaid'  # Will be paid on delivery
                else:
                    order.status = 'paid'  # Assume paid if slip uploaded
                order.save()
                    
                # Update cart status to mark as ordered
                cart_items.update(status='notin_cart')

                return redirect('home')

        except CustomUser.DoesNotExist:
            return redirect('login')

class OrderHistoryView(View):
    def get(self, request, user):
        try:
            user_obj = CustomUser.objects.get(id=user)
            orders = Order.objects.filter(user=user_obj).order_by("-order_date").select_related('cart', 'cart__book')
            
            # Group orders by payment method and date for better display
            order_groups = {}
            for order in orders:
                date_key = order.order_date.strftime('%Y-%m-%d %H:%M')
                if date_key not in order_groups:
                    order_groups[date_key] = []
                order_groups[date_key].append(order)
            
            context = {
                "orders": orders,
                "order_groups": order_groups,
                "user_obj": user_obj,
                "total_orders": orders.count(),
            }
            return render(request, "home/orderhistory.html", context)
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

class AddToCartView(View):
    """View to add books to cart for testing multiple orders"""
    def post(self, request, user_id, book_id):
        try:
            user_obj = CustomUser.objects.get(id=user_id)
            book = Book.objects.get(id=book_id)
            
            # Check if item already exists in cart
            existing_cart = Cart.objects.filter(
                user=user_obj, 
                book=book, 
                status='in_cart'
            ).first()
            
            if existing_cart:
                # Update quantity
                existing_cart.quantity += 1
                existing_cart.total_price = existing_cart.price * existing_cart.quantity
                existing_cart.save()
            else:
                # Create new cart item
                Cart.objects.create(
                    user=user_obj,
                    book=book,
                    quantity=1,
                    price=book.price,
                    total_price=book.price,
                    status='in_cart'
                )
            
            return redirect('cart', user=user_id)
        except (CustomUser.DoesNotExist, Book.DoesNotExist):
            return redirect('book')

class CreateSampleCartView(View):
    """View to create sample cart items for testing"""
    def get(self, request, user_id):
        try:
            user_obj = CustomUser.objects.get(id=user_id)
            books = Book.objects.all()[:3]  # Get first 3 books
            
            # Clear existing cart
            Cart.objects.filter(user=user_obj, status='in_cart').delete()
            
            # Create sample cart items
            for i, book in enumerate(books, 1):
                Cart.objects.create(
                    user=user_obj,
                    book=book,
                    quantity=i,  # Different quantities: 1, 2, 3
                    price=book.price,
                    total_price=book.price * i,
                    status='in_cart'
                )
            
            return redirect('cart', user=user_id)
        except CustomUser.DoesNotExist:
            return redirect('login')
