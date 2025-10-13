from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    phone = models.CharField(max_length=20, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    province = models.CharField(max_length=100, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)

    def __str__(self):
        return self.username

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
    sold = models.PositiveIntegerField(default=0)
    rating_average = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    rating_count = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField('BookCategory', blank=True)

    def __str__(self):
        return self.title

class BookCategory(models.Model):
    category_name = models.CharField(max_length=150, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.category_name

class Cart(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='in_cart')  # in_cart, notin_cart

    def __str__(self):
        return f'Cart {self.id} for {self.user.username}'

class Order(models.Model):
    class orderstatus(models.TextChoices):
        UNPAID = 'unpaid', 'ยังไม่ชำระเงิน'
        PAID = 'paid', 'ชำระเงินแล้ว'
        PROCESSING = 'processing', 'กำลังเตรียมสินค้า'
        SHIPPED = 'shipped', 'กำลังจัดส่ง'
        DELIVERED = 'delivered', 'จัดส่งสำเร็จ'
        CANCELLED = 'cancelled', 'ยกเลิก'
        REFUNDED = 'refunded', 'คืนเงิน'
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=orderstatus.choices, default=orderstatus.PAID)

    def __str__(self):
        return f'Order {self.id} for {self.cart}'

class Payment(models.Model):
    class paymentmethod(models.TextChoices):
        BANK = 'bank', 'โอนเงินผ่านธนาคาร'
        PROMPTPAY = 'promptpay', 'พร้อมเพย์'
        CASH = 'cash', 'เก็บเงินปลายทาง'
    
    class paymentstatus(models.TextChoices):
        PENDING = 'pending', 'รอตรวจสอบ'
        APPROVED = 'approved', 'อนุมัติแล้ว'
        REJECTED = 'rejected', 'ปฏิเสธ'

    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    payment_slip = models.FileField(upload_to="payment/", null=True, blank=True)
    payment_date = models.DateTimeField()
    method = models.CharField(max_length=20, choices=paymentmethod.choices)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=paymentstatus.choices, default=paymentstatus.PENDING)
    verified_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f'Payment {self.id} for Order {self.order.id}'

class Review(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField(max_length=500, blank=True)
    created_date = models.DateTimeField()

    def __str__(self):
        return f'Review by {self.user.first_name} for {self.book.title} ({self.rating} stars)'
