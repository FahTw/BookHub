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
            if user.is_staff:
                return redirect('/dashboard')
            else:
                return redirect('/home')
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

            context = {
                "orders": orders,
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
            cart_info = order_obj.cart
            payment_info = Payment.objects.get(order=order_obj)
            
            context = {
                "user_obj": user_obj,
                "order": order_obj,
                "cart_info": cart_info,
                "payment_info": payment_info,
            }
            return render(request, "home/orderhistory_detail.html", context)
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

class DashboardView(View, LoginRequiredMixin):
    def get(self, request):
        # Get statistics for dashboard
        total_orders = Order.objects.count()
        total_revenue = Order.objects.filter(status='paid').aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        pending_orders = Order.objects.filter(status='unpaid').count()
        total_books = Book.objects.count()
        total_users = CustomUser.objects.count()
        recent_orders = Order.objects.all().order_by('-order_date')[:5].select_related('user', 'cart', 'cart__book')
        popular_books = Book.objects.order_by('-sold')[:5]
        
        context = {
            'total_orders': total_orders,
            'total_revenue': total_revenue,
            'pending_orders': pending_orders,
            'total_books': total_books,
            'total_users': total_users,
            'recent_orders': recent_orders,
            'popular_books': popular_books,
        }
        return render(request, 'owner/dashboard.html', context)

class OrderHistoryOwnerView(View, LoginRequiredMixin):
    def get(self, request):
        # Get all orders for owner view
        orders = Order.objects.all().order_by('-order_date').select_related('user', 'cart', 'cart__book')
        
        # Get filter parameters
        status_filter = request.GET.get('status', '')
        search_query = request.GET.get('search', '')
        
        # Apply filters
        if status_filter:
            orders = orders.filter(status=status_filter)
        
        if search_query:
            orders = orders.filter(
                Q(cart__book__title__icontains=search_query) | 
                Q(user__first_name__icontains=search_query) |
                Q(user__last_name__icontains=search_query) |
                Q(user__email__icontains=search_query)
            )
        
        # Calculate statistics for cards
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status__in=['unpaid', 'paid']).count()
        shipping_orders = Order.objects.filter(status__in=['processing', 'shipped']).count()
        completed_orders = Order.objects.filter(status='delivered').count()
        
        context = {
            'orders': orders,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'shipping_orders': shipping_orders,
            'completed_orders': completed_orders,
            'status_filter': status_filter,
            'search_query': search_query,
        }
        return render(request, 'owner/orderhistory_owner.html', context)

class OrderHistoryOwnerDetailView(View, LoginRequiredMixin):
    def get(self, request, order):
        try:
            order_obj = Order.objects.get(id=order)
            cart_info = order_obj.cart
            user_info = order_obj.user
            
            # Try to get payment information
            try:
                payment_info = Payment.objects.get(order=order_obj)
            except Payment.DoesNotExist:
                payment_info = None
            
            context = {
                'order': order_obj,
                'cart_info': cart_info,
                'user_info': user_info,
                'payment_info': payment_info,
            }
            return render(request, 'owner/orderhistory_detail_owner.html', context)
        except Order.DoesNotExist:
            return redirect('order_history_owner')
    
    def post(self, request, order):
        try:
            order_obj = Order.objects.get(id=order)
            new_status = request.POST.get('status')
            
            # Update order status directly from form
            if new_status in ['unpaid', 'paid', 'processing', 'shipped', 'delivered', 'cancelled']:
                order_obj.status = new_status
                order_obj.save()
                
                # Also update payment status if changing to paid
                if new_status == 'paid':
                    try:
                        payment = Payment.objects.get(order=order_obj)
                        payment.status = 'approved'
                        payment.verified_date = datetime.now()
                        payment.save()
                    except Payment.DoesNotExist:
                        pass
            
            # Redirect back to order list after update
            return redirect('order_history_owner')
        except Order.DoesNotExist:
            return redirect('order_history_owner')
