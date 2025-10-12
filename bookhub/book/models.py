from django.db import models
from django.contrib.auth.models import AbstractUser

# class User(models.Model):
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     email = models.EmailField(unique=True, null=True, blank=True)
#     phone = models.CharField(max_length=20, null=True, blank=True)
#     password = models.CharField(max_length=150)
#     role = models.CharField(max_length=50, default='user', choices=[
#         ('user', 'ลูกค้า'),
#         ('admin', 'ผู้ดูแลระบบ')
#     ])

#     def __str__(self):
#         return f'{self.first_name} {self.last_name}'

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)

class Book(models.Model):
    title = models.CharField(max_length=200)
    image = models.FileField(upload_to="book/", null=True, blank=True)
    author = models.CharField(max_length=150)
    publisher = models.CharField(max_length=150, null=True, blank=True)
    publication_date = models.DateField(null=True, blank=True)
    pages = models.PositiveIntegerField(null=True, blank=True)
    language = models.CharField(max_length=50, default='ไทย')
    detail = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    sold_count = models.PositiveIntegerField(default=0)
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    rating_count = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField('BookCategory', related_name='books', blank=True)

    def __str__(self):
        return self.title

class BookCategory(models.Model):
    category_name = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.category_name

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart {self.id} for {self.user}'

class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} of {self.book.title} in Cart {self.cart.id}'

class Order(models.Model):

    STATUS_CHOICES = [
        ('pending', 'รอดำเนินการ'),
        ('paid', 'ชำระเงินแล้ว'),
        ('processing', 'กำลังเตรียมสินค้า'),
        ('shipped', 'กำลังจัดส่ง'),
        ('delivered', 'จัดส่งสำเร็จ'),
        ('cancelled', 'ยกเลิก'),
        ('refunded', 'คืนเงิน')
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    shipping_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    final_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f'Order {self.id} for {self.user}'

class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'{self.quantity} of {self.book.title} in Order {self.order.id}'

class Payment(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('bank_transfer', 'โอนเงินผ่านธนาคาร'),
        ('promptpay', 'พร้อมเพย์'),
        ('cash_on_delivery', 'เก็บเงินปลายทาง')
    ]

    STATUS_CHOICES = [
        ('pending', 'รอตรวจสอบ'),
        ('approved', 'อนุมัติแล้ว'),
        ('rejected', 'ปฏิเสธ')
    ]

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_slip = models.FileField(upload_to="payment/", null=True, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    verified_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Payment {self.id} for Order {self.order.id}'

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(max_length=500, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Review by {self.user.get_full_name()} for {self.book.title} ({self.rating} stars)'
