from django.shortcuts import render, redirect
from django.views import View
from django.db.models import *
from book.models import *
from book.forms import *
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(View):
    def get(self, request):
        form = AuthenticationForm()
        return render(request, 'login/login.html', {'form': form})
    
    def post(self, request):
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user() 
            login(request, user)
            return redirect('dashboard' if user.is_staff else 'home')
        return render(request, 'login/login.html', {'form': form})

class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('login')

class RegisterView(View):
    def get(self, request):
        form = UserRegistrationForm()
        return render(request, 'login/register.html', {'form': form})
    
    def post(self, request):
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password1'])
            user.save()
            return redirect('login')
        return render(request, 'login/register.html', {'form': form})

class HomeView(View, LoginRequiredMixin):
    def get(self, request):
        categories = BookCategory.objects.all()
        best_sellers = Book.objects.all().order_by('-sold')[:5]
        best_reviews = Review.objects.select_related('book', 'user').order_by('-rating', '-created_date')[:5]
        
        context = {
            'categories': categories,
            'best_sellers': best_sellers,
            'best_reviews': best_reviews,
        }
        return render(request, 'home/home.html', context)

class ProfileView(View, LoginRequiredMixin):
    def get(self, request):
        form = UserProfileForm(instance=request.user)
        return render(request, 'home/profile.html', {'form': form})

    def post(self, request):
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')
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

class CategoryView(View, LoginRequiredMixin):
    def get(self, request, category_id):
        category = BookCategory.objects.get(pk=category_id)
        books = Book.objects.filter(categories=category)
        categories = BookCategory.objects.all()
        return render(request, 'home/category.html', {
            'category': category,
            'books': books,
            'categories': categories
        })

class CartView(View, LoginRequiredMixin):
    def get(self, request, user):
        try:
            user = CustomUser.objects.get(id=user)
            cart = Cart.objects.filter(user=user, status='in_cart').select_related('book')

            # Calculate totals
            total_amount = sum(item.total_price for item in cart)
            total_items = sum(item.quantity for item in cart)

            context = {
                'user': user,
                'cart': cart,
                'total_amount': total_amount,
                'total_items': total_items,
            }
            return render(request, 'payment/cart.html', context)
        except CustomUser.DoesNotExist:
            return redirect('login')

    def post(self, request, user):
        try:
            user_obj = CustomUser.objects.get(id=user)
            action = request.POST.get('action')
            cart_id = request.POST.get('cart_id')
            
            if action == 'remove' and cart_id:
                Cart.objects.filter(id=cart_id, user=user_obj).delete()
            
            elif action == 'update' and cart_id:
                quantity_change = int(request.POST.get('quantity_change', 0))
                cart_item = Cart.objects.get(id=cart_id, user=user_obj)
                new_quantity = cart_item.quantity + quantity_change
                
                if 0 < new_quantity <= cart_item.book.stock:
                    cart_item.quantity = new_quantity
                    cart_item.total_price = cart_item.price * cart_item.quantity
                    cart_item.save()
            
            return redirect('cart', user=user)
        except (CustomUser.DoesNotExist, Cart.DoesNotExist):
            return redirect('login')

class AddToCartView(View, LoginRequiredMixin):
    def post(self, request, book_id):        
        try:
            book = Book.objects.get(id=book_id)
            user = request.user
            
            # Check if the book is already in the cart
            cart_item, created = Cart.objects.get_or_create(
                user=user,
                book=book,
                status='in_cart',
                defaults={'quantity': 1, 'price': book.price, 'total_price': book.price}
            )
            
            if not created:
                # If it already exists, increase the quantity
                if cart_item.quantity < book.stock:
                    cart_item.quantity += 1
                    cart_item.total_price = cart_item.price * cart_item.quantity
                    cart_item.save()
            
            return redirect('cart', user=user.id)
        except Book.DoesNotExist:
            return redirect('home')

class PaymentView(View, LoginRequiredMixin):
    def get(self, request, user):
        try:
            user_obj = CustomUser.objects.get(id=user)
            cart_items = Cart.objects.filter(user=user_obj, status='in_cart')
            total_amount = sum(item.total_price for item in cart_items)
            
            context = {
                'user_obj': user_obj,
                'cart_items': cart_items,
                'total_amount': total_amount,
            }
            return render(request, 'payment/payment.html', context)
        except CustomUser.DoesNotExist:
            return redirect('login')
    
    def post(self, request, user):
        try:
            user_obj = CustomUser.objects.get(id=user)
            cart_items = Cart.objects.filter(user=user_obj, status='in_cart')
            payment_method = request.POST.get('method')

            for cart_item in cart_items:
                # Create Order
                order = Order.objects.create(
                    user=user_obj,
                    cart=cart_item,
                    order_date=datetime.now(),
                    total_amount=cart_item.total_price,
                    status='unpaid' if payment_method == 'cash' else 'paid'
                )
                        
                # Create Payment
                payment = Payment.objects.create(
                    order=order,
                    payment_date=datetime.now(),
                    method=payment_method,
                    amount=cart_item.total_price,
                    status='pending'
                )

                # Add payment slip if uploaded
                if payment_method != 'cash' and 'payment_slip' in request.FILES:
                    payment.payment_slip = request.FILES['payment_slip']
                    payment.save()

                # Update order status based on payment method
                if payment_method == 'cash':
                    order.status = 'unpaid'  # Will be paid on delivery
                else:
                    order.status = 'paid'  # Assume paid if slip uploaded
                order.save()
            
            # Update cart status AFTER all orders are created successfully
            cart_items.update(status='notin_cart')
            return redirect('home')

        except CustomUser.DoesNotExist:
            return redirect('login')

class OrderHistoryView(View, LoginRequiredMixin):
    def get(self, request, user):
        try:
            user_obj = CustomUser.objects.get(id=user)
            orders = Order.objects.filter(user=user_obj).order_by('-order_date').select_related('cart', 'cart__book')

            context = {
                'orders': orders,
                'user_obj': user_obj,
                'total_orders': orders.count(),
            }
            return render(request, 'home/orderhistory.html', context)
        except CustomUser.DoesNotExist:
            return redirect('login')

class OrderHistoryDetailView(View, LoginRequiredMixin):
    def get(self, request, user, order):
        try:
            user_obj = CustomUser.objects.get(id=user)
            order_obj = Order.objects.get(id=order, user=user_obj)
            cart_info = order_obj.cart
            payment_info = Payment.objects.get(order=order_obj)
            
            context = {
                'user_obj': user_obj,
                'order': order_obj,
                'cart_info': cart_info,
                'payment_info': payment_info,
            }
            return render(request, 'home/orderhistory_detail.html', context)
        except (CustomUser.DoesNotExist, Order.DoesNotExist):
            return redirect('login')

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

class ManageBookListView(View, LoginRequiredMixin):
    def get(self, request):
        books = Book.objects.all().order_by('-id')
        search_query = request.GET.get('search', '')
        
        # Apply search filter
        if search_query:
            books = books.filter(
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(publisher__icontains=search_query)
            )
        
        # Calculate statistics
        total_books = Book.objects.count()
        low_stock_count = Book.objects.filter(stock__lt=10).count()
        out_of_stock_count = Book.objects.filter(stock=0).count()
        total_value = Book.objects.aggregate(
            total=Sum(F('stock') * F('price'), output_field=models.DecimalField())
        )['total'] or 0
        
        categories = BookCategory.objects.all().order_by('category_name')
        
        context = {
            'books': books,
            'total_books': total_books,
            'low_stock_count': low_stock_count,
            'out_of_stock_count': out_of_stock_count,
            'total_value': total_value,
            'search_query': search_query,
            'categories': categories,
        }
        return render(request, 'owner/book_manage.html', context)
    
    def post(self, request):
        # Check if this is a category creation request
        if 'category_name' in request.POST:
            category_form = BookCategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('managelist_book')
        
        # Handle book creation
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('managelist_book')
        
        # If form is invalid, return with errors
        books = Book.objects.all().order_by('-id')
        categories = BookCategory.objects.all().order_by('category_name')
        
        context = {
            'books': books,
            'categories': categories,
            'form': form,
            'total_books': Book.objects.count(),
            'low_stock_count': Book.objects.filter(stock__lt=10).count(),
            'out_of_stock_count': Book.objects.filter(stock=0).count(),
            'total_value': Book.objects.aggregate(
                total=Sum(F('stock') * F('price'), output_field=models.DecimalField())
            )['total'] or 0,
        }
        return render(request, 'owner/book_manage.html', context)

class ManageBookView(View, LoginRequiredMixin):
    def get(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        form = BookForm(instance=book)
        return render(request, 'owner/edit_book.html', {'form': form, 'book': book})

    def post(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('managelist_book')
        return render(request, 'owner/edit_book.html', {'form': form, 'book': book})

class ManageBookDeleteView(View, LoginRequiredMixin):
    def get(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        book.delete()
        return redirect('managelist_book')

class OrderHistoryOwnerView(View, LoginRequiredMixin):
    def get(self, request):
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
        
        # Calculate statistics
        context = {
            'orders': orders,
            'total_orders': Order.objects.count(),
            'pending_orders': Order.objects.filter(status__in=['unpaid', 'paid']).count(),
            'shipping_orders': Order.objects.filter(status__in=['processing', 'shipped']).count(),
            'completed_orders': Order.objects.filter(status='delivered').count(),
            'status_filter': status_filter,
            'search_query': search_query,
        }
        return render(request, 'owner/orderhistory_owner.html', context)

class OrderHistoryOwnerDetailView(View, LoginRequiredMixin):
    def get(self, request, order):
        try:
            order_obj = Order.objects.get(id=order)
            payment_info = None
            
            try:
                payment_info = Payment.objects.get(order=order_obj)
            except Payment.DoesNotExist:
                pass
            
            context = {
                'order': order_obj,
                'cart_info': order_obj.cart,
                'user_info': order_obj.user,
                'payment_info': payment_info,
            }
            return render(request, 'owner/orderhistory_detail_owner.html', context)
        except Order.DoesNotExist:
            return redirect('order_history_owner')
    
    def post(self, request, order):
        try:
            order_obj = Order.objects.get(id=order)
            new_status = request.POST.get('status')
            
            # Update order status
            if new_status in ['unpaid', 'paid', 'processing', 'shipped', 'delivered', 'cancelled']:
                order_obj.status = new_status
                order_obj.save()
                
                # Update payment status if changing to paid
                if new_status == 'paid':
                    try:
                        payment = Payment.objects.get(order=order_obj)
                        payment.status = 'approved'
                        payment.verified_date = datetime.now()
                        payment.save()
                    except Payment.DoesNotExist:
                        pass
            
            return redirect('order_history_owner')
        except Order.DoesNotExist:
            return redirect('order_history_owner')

class UserListView(LoginRequiredMixin, View):
    def get(self, request):
        users = CustomUser.objects.all().order_by('-date_joined')
        search_query = request.GET.get('search', '')
        
        # Apply search filter
        if search_query:
            users = users.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        
        # Calculate statistics
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        context = {
            'users': users,
            'total_users': CustomUser.objects.count(),
            'regular_users': CustomUser.objects.filter(is_staff=False).count(),
            'admin_users': CustomUser.objects.filter(is_staff=True).count(),
            'new_users_this_month': CustomUser.objects.filter(date_joined__gte=first_day_of_month).count(),
            'search_query': search_query,
        }
        return render(request, 'owner/user_list.html', context)

class UserView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = CustomUser.objects.get(pk=user_id)
        if not user.is_staff:
            user.delete()
        return redirect('user_list')

class UserDetailView(LoginRequiredMixin, View):
    def get(self, request, user_id):
        user = CustomUser.objects.get(pk=user_id)
        user_orders = Order.objects.filter(user=user)
        
        context = {
            'user_detail': user,
            'total_orders': user_orders.count(),
            'total_spent': user_orders.filter(
                status__in=['paid', 'processing', 'shipped', 'delivered']
            ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            'recent_orders': user_orders.order_by('-order_date')[:5],
        }
        return render(request, 'owner/user_detail.html', context)

class StatView(View, LoginRequiredMixin):
    def get(self, request):
        # Overall statistics
        total_books = Book.objects.count()
        total_revenue = Order.objects.filter(
            status__in=['paid', 'processing', 'shipped', 'delivered']
        ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0
        total_orders = Order.objects.filter(
            status__in=['paid', 'processing', 'shipped', 'delivered']
        ).count()
        total_books_sold = Book.objects.aggregate(Sum('sold'))['sold__sum'] or 0
        
        # Top selling books
        top_selling_books = Book.objects.all().order_by('-sold')[:10]
        
        # Books by category with sales
        category_stats = BookCategory.objects.annotate(
            total_books=Count('book'),
            total_sold=Sum('book__sold'),
            total_revenue=Sum(
                Case(
                    When(
                        book__cart__order__status__in=['paid', 'processing', 'shipped', 'delivered'], 
                        then=F('book__cart__total_price')
                    ),
                    default=0,
                    output_field=models.DecimalField()
                )
            )
        ).order_by('-total_sold')
        
        # Low stock books
        low_stock_books = Book.objects.filter(stock__lt=10).order_by('stock')[:10]
        
        context = {
            'total_books': total_books,
            'total_revenue': total_revenue,
            'total_orders': total_orders,
            'total_books_sold': total_books_sold,
            'top_selling_books': top_selling_books,
            'category_stats': category_stats,
            'low_stock_books': low_stock_books,
        }
        
        return render(request, 'owner/stat.html', context)
