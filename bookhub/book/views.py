from django.shortcuts import render, redirect
from django.views import View
from django.db.models import *
from book.models import *
from book.forms import *
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout

class LoginView(View):
    def get(self, request):
        # ดึงฟอร์ม authen ของ Django มาใช้
        form = AuthenticationForm()
        return render(request, 'login/login.html', {'form': form})

    def post(self, request):
        # ตรวจสอบข้อมูลที่ผู้ใช้กรอกมา
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # ดึงข้อมูลผู้ใช้จากฟอร์ม และเข้าสู่ระบบ
            user = form.get_user() 
            login(request, user)
            # role redirect
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

# ดึงข้อมูลมาแสดงในหน้า Home
class HomeView(View):
    def get(self, request):
        # หมวดหมู่หนังสือ, หนังสือขายดี, รีวิวที่ดีท
        categories = BookCategory.objects.all()
        # เรียงลำดับยอดหนังสือที่ขายได้จากมากไปน้อย 5 เล่ม
        best_sellers = Book.objects.all().order_by('-sold')[:5]
        # รีวิวที่ได้คะแนนสูงสุด 5 รีวิว
        best_reviews = Review.objects.select_related('book', 'user').order_by('-rating', '-created_date')[:5]
        # ส่งข้อมูลไปที่ template
        context = {
            'categories': categories,
            'best_sellers': best_sellers,
            'best_reviews': best_reviews,
        }
        return render(request, 'home/home.html', context)

class ProfileView(View):
    def get(self, request):
        # ดึงข้อมูลมาใส่ในฟอร์ม instance เพื่อดึงข้อมูลเดิมมาแสดง
        form = UserProfileForm(instance=request.user)
        return render(request, 'home/profile.html', {'form': form})

    def post(self, request):
        # instance เพื่ออัปเดตข้อมูลเดิม
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            # บันทึกข้อมูลลง db
            form.save()
            return redirect('profile')
        # เอาไปแสดงใน template 
        return render(request, 'home/profile.html', {'form': form})

class BookListView(View):
    # แสดงรายการหนังสือทั้งหมด
    def get(self, request):
        books = Book.objects.all()
        return render(request, 'home/book_list.html', {'books': books})

class BookDetailView(View):
    # ดึงข้อมูลของหนังสือแต่ละเล่มมาแสดง
    def get(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        # ดึงข้อมูลรีวิวของผู user ที่เขียนไว้โดยเรียงตามวันที่ล่าสุด
        reviews = Review.objects.filter(book=book).select_related('user').order_by('-created_date')
        review_stats = reviews.aggregate(
            avg_rating=Avg('rating'),
            review_count=Count('id')
        )
        # แสดงผลคะแนนเฉลี่ยและจำนวนคอมเมนต์, ยอดขาย
        book.rating = round(review_stats['avg_rating'], 1) if review_stats['avg_rating'] else 0.0
        book.comment_count = review_stats['review_count']
        book.sold_count = book.sold

        # ดึงฟอร์มสำหรับเขียนรีวิว
        form = ReviewForm()
        return render(request, 'home/book_detail.html', {
            'book': book,
            'reviews': reviews,
            'form': form
        })

    # review
    def post(self, request, book_id):
        book = Book.objects.get(pk=book_id)
        form = ReviewForm(request.POST)
        reviews = Review.objects.filter(book=book).select_related('user').order_by('-created_date')
        
        if form.is_valid():
            # 
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            
            # Update book rating
            review_stats = reviews.aggregate(
                avg_rating=Avg('rating'),
                review_count=Count('id')
            )
            # ถ้าไม่ได้ให้ก้ set เป็น 0
            book.rating_average = review_stats['avg_rating'] or 0
            book.rating_count = review_stats['review_count']
            book.save(update_fields=['rating_average', 'rating_count'])
            
            return redirect('book_detail', book_id=book_id)

        return render(request, 'home/book_detail.html', {
            'book': book,
            'reviews': reviews,
            'form': form
        })

# ดึงข้อมูลหมวดหมู่หนังสือ
class CategoryView(View):
    def get(self, request, category_id):
        # ดึงมาจาก cate id
        category = BookCategory.objects.get(pk=category_id)
        # หาหนังสือตแต่ละเล่มของหมวดหมู่
        books = Book.objects.filter(categories=category)
        # ดึงข้อมูลหมวดหมู่ทั้งหมด
        categories = BookCategory.objects.all()
        # ส่งเทมเพลต
        return render(request, 'home/category.html', {
            'category': category,
            'books': books,
            'categories': categories
        })

class CartView(View):
    def get(self, request, user):
        user_obj = CustomUser.objects.get(id=user)
        cart = Cart.objects.filter(user=user_obj, status='in_cart').select_related('book')

        # Calculate totals
        total_amount = sum(item.total_price for item in cart)
        total_items = sum(item.quantity for item in cart)

        context = {
            'user': user_obj,
            'cart': cart,
            'total_amount': total_amount,
            'total_items': total_items,
        }
        return render(request, 'payment/cart.html', context)

    def post(self, request, user):
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

class AddToCartView(View):
    def post(self, request, book_id):
        book = Book.objects.get(id=book_id)
        user = request.user
            
        # Check if the book is already in the cart
        cart_item, created = Cart.objects.get_or_create(
            user=user,
            book=book,
            status='in_cart',
            defaults={'quantity': 1, 'price': book.price, 'total_price': book.price}
        )
            
        # If it already exists, increase the quantity
        if not created and cart_item.quantity < book.stock:
            cart_item.quantity += 1
            cart_item.total_price = cart_item.price * cart_item.quantity
            cart_item.save()

        return redirect('cart', user=user.id)

class PaymentView(View):
    def get(self, request, user):
        user_obj = CustomUser.objects.get(id=user)
        cart_items = Cart.objects.filter(user=user_obj, status='in_cart').select_related('book')
        total_amount = sum(item.total_price for item in cart_items)
            
        context = {
            'user_obj': user_obj,
            'cart_items': cart_items,
            'total_amount': total_amount,
        }
        return render(request, 'payment/payment.html', context)

    def post(self, request, user):
        user_obj = CustomUser.objects.get(id=user)
        cart_items = Cart.objects.filter(user=user_obj, status='in_cart')
        payment_method = request.POST.get('method')
        payment_slip = request.FILES.get('payment_slip')

        for cart_item in cart_items:
            # Determine order status based on payment method
            order_status = 'unpaid' if payment_method == 'cash' else 'paid'
            
            # Create Order
            order = Order.objects.create(
                user=user_obj,
                cart=cart_item,
                order_date=datetime.now(),
                total_amount=cart_item.total_price,
                status=order_status
            )

            # Create Payment
            Payment.objects.create(
                order=order,
                payment_date=datetime.now(),
                method=payment_method,
                amount=cart_item.total_price,
                status='pending',
                payment_slip=payment_slip if payment_method != 'cash' and payment_slip else None
            )

        # Update all cart items to notin_cart
        cart_items.update(status='notin_cart')
        
        return redirect('home')

class OrderHistoryView(View):
    def get(self, request, user):
        user_obj = CustomUser.objects.get(id=user)
        orders = Order.objects.filter(user=user_obj).order_by('-order_date').select_related('cart', 'cart__book')

        context = {
            'orders': orders,
            'user_obj': user_obj,
            'total_orders': orders.count(),
        }
        return render(request, 'home/orderhistory.html', context)

    def post(self, request, user):
        user_obj = CustomUser.objects.get(id=user)
        order_id = request.POST.get('order_id')
        
        if order_id:
            order_obj = Order.objects.get(id=order_id, user=user_obj)
            # Only allow cancellation for paid or processing orders
            if order_obj.status in ['paid', 'processing']:
                order_obj.status = 'cancelled'
                order_obj.save()
                # Update payment status
                payment = Payment.objects.filter(order=order_obj).first()
                if payment:
                    payment.status = 'cancelled'
                    payment.save()
        
        return redirect('order_history_user', user=user)

class OrderHistoryDetailView(View):
    def get(self, request, user, order):
        user_obj = CustomUser.objects.get(id=user)
        order_obj = Order.objects.get(id=order, user=user_obj)
        payment_info = Payment.objects.filter(order=order_obj).first()
            
        context = {
            'user_obj': user_obj,
            'order': order_obj,
            'cart_info': order_obj.cart,
            'payment_info': payment_info,
        }
        return render(request, 'home/orderhistory_detail.html', context)


class DashboardView(View):
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

class ManageBookListView(View):
    # แสดงรายการหนังสือทั้งหมด
    def get(self, request):
        books = Book.objects.all().order_by('-id')
        search_query = request.GET.get('search', '')
        
        # ทำเสิชฟิลเตอร์
        if search_query:
            books = books.filter(
                # ใช้ Q เพื่อค้นหาหลายฟิลด์
                Q(title__icontains=search_query) |
                Q(author__icontains=search_query) |
                Q(publisher__icontains=search_query)
            )
        
        # สถิติหนังสือ
        # รวมหนังสือทั้งหมด, สินค้าคงเหลือต่ำกว่า 10, สินค้าหมด, มูลค่าคงเหลือ
        total_books = Book.objects.count()
        low_stock_count = Book.objects.filter(stock__lt=10).count()
        out_of_stock_count = Book.objects.filter(stock=0).count()
        
        # สร้าง col total ทิพย์ไว้เพื่อคำนวณมูลค่ารวม
        total_value = Book.objects.aggregate(
            # stock * price
            total=Sum(F('stock') * F('price'), output_field=models.DecimalField())
        )['total'] or 0
        
        # category ทั้งหมด
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
    
    # create book
    def post(self, request):
        # เช็คว่ามีการส่งฟอร์มเพิ่มหมวดหมู่หนังสือมาหรือไม่
        if 'category_name' in request.POST:
            category_form = BookCategoryForm(request.POST)
            if category_form.is_valid():
                category_form.save()
                return redirect('managelist_book')
        
        # เรียกฟอร์มเพื่อเพิ่มหนังสือ
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('managelist_book')
        
        #ดึงหนังสือและหมวดหมู่ทั้งหมด
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


class ManageBookView(View):
    # ดดึงข้อมูลหนังสือมาแสดงในฟอร์ม
    def get(self, request, book_id):
        # ดึงข้อมูลหนังสือที่ต้องการดูหน้า edit
        book = Book.objects.get(pk=book_id)
        # ดึงข้อมูลมาใส่ในฟอร์ม instance เพื่อดึงข้อมูลเดิมมาแสดง
        form = BookForm(instance=book)
        return render(request, 'owner/edit_book.html', {'form': form, 'book': book})

    def post(self, request, book_id):
        # ดึงข้อมูลหนังสือที่ต้องการแก้ไข
        book = Book.objects.get(pk=book_id)
        # ดึงข้อมูลมาใส่ในฟอร์ม instance เพื่อดึงข้อมูลเดิมมาอัปเดตข้อมูล
        form = BookForm(request.POST, request.FILES, instance=book)
        if form.is_valid():
            form.save()
            return redirect('managelist_book')
        return render(request, 'owner/edit_book.html', {'form': form, 'book': book})

class ManageBookDeleteView(View):
    # ลบหนังสือ
    def get(self, request, book_id):
        # ดึงข้อมูลหนังสือที่ต้องการลบ
        book = Book.objects.get(pk=book_id)
        book.delete()
        return redirect('managelist_book')

class OrderHistoryOwnerView(View):
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

class OrderHistoryOwnerDetailView(View):
    def get(self, request, order):
        order_obj = Order.objects.get(id=order)
        payment_info = Payment.objects.filter(order=order_obj).first()

        context = {
            'order': order_obj,
            'cart_info': order_obj.cart,
            'user_info': order_obj.user,
            'payment_info': payment_info,
        }
        return render(request, 'owner/orderhistory_detail_owner.html', context)

    def post(self, request, order):
        order_obj = Order.objects.get(id=order)
        payment = Payment.objects.filter(order=order_obj).first()
        
        # Handle payment status update
        payment_status = request.POST.get('payment_status')
        if payment_status and payment:
            if payment_status == 'paid':
                payment.status = 'paid'
                payment.verified_date = datetime.now()
                payment.save()
                # Update order status to paid if currently unpaid
                if order_obj.status == 'unpaid':
                    order_obj.status = 'paid'
                    order_obj.save()
                    
            elif payment_status == 'cancelled':
                payment.status = 'cancelled'
                payment.save()
                # Update order status to cancelled
                order_obj.status = 'cancelled'
                order_obj.save()
            
            return redirect('order_history_owner_detail', order=order)
        
        # Handle order status update
        new_status = request.POST.get('status')
        if new_status in ['unpaid', 'paid', 'processing', 'shipped', 'delivered', 'cancelled']:
            order_obj.status = new_status
            order_obj.save()

            # Update payment status accordingly
            if payment:
                if new_status == 'paid':
                    payment.status = 'paid'
                    payment.verified_date = datetime.now()
                    payment.save()
                elif new_status == 'cancelled':
                    payment.status = 'cancelled'
                    payment.save()
            
            return redirect('order_history_owner_detail', order=order)

        return redirect('order_history_owner_detail', order=order)

class UserListView(View):
    def get(self, request):
        users = CustomUser.objects.all().order_by('-date_joined')
        search_query = request.GET.get('search', '')
        
        # เสิชข้อมูล user
        if search_query:
            users = users.filter(
                Q(first_name__icontains=search_query) |
                Q(last_name__icontains=search_query) |
                Q(username__icontains=search_query) |
                Q(email__icontains=search_query)
            )
        # นับวันที่ 1 ของเดือนปัจจุบัน
        first_day_of_month = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        
        context = {
            # user ทั้งหมด, user ปกติ, user admin
            'users': users,
            'total_users': CustomUser.objects.count(),
            'regular_users': CustomUser.objects.filter(is_staff=False).count(),
            'admin_users': CustomUser.objects.filter(is_staff=True).count(),
            # คำนวณผู้ใช้ใหม่ในเดือนนี้
            'new_users_this_month': CustomUser.objects.filter(date_joined__gte=first_day_of_month).count(),
            'search_query': search_query,
        }
        return render(request, 'owner/user_list.html', context)

class UserView(View):
    # ส่วนของการลบ user
    def get(self, request, user_id):
        user = CustomUser.objects.get(pk=user_id)
        # ถ้าไม่เป็น admin ถึงจะลบได้
        if not user.is_staff:
            user.delete()
        return redirect('user_list')
    
class UserDetailView(View):
    # ดึงข้อมูล user มาแสดงเป็นรายคน
    def get(self, request, user_id):
        # ดึงขข้อมูล user รายคนและ order ที่เคยสั่ง
        user = CustomUser.objects.get(pk=user_id)
        user_orders = Order.objects.filter(user=user)
        
        context = {
            'user_detail': user,
            'total_orders': user_orders.count(),
            # ยอดซื้อรวมที่เคยสั่ง โดยให้อยู่ในสถานะที่ระบุ
            'total_spent': user_orders.filter(
                status__in=['paid', 'processing', 'shipped', 'delivered']
            # รวมยอดถ้าไม่มีให้เป็น 0
            ).aggregate(Sum('total_amount'))['total_amount__sum'] or 0,
            # ประวัติการสั่งซื้อล่าสุด 5 รายการ
            'recent_orders': user_orders.order_by('-order_date')[:5],
        }
        return render(request, 'owner/user_detail.html', context)

class StatView(View):
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
