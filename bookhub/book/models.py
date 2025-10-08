from django.db import models

class User(models.Model):
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, null=True, blank=True)
    password = models.CharField(max_length=150)
    role = models.CharField(max_length=50, default='user')
    address = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
    
class Book(models.Model):
    title = models.CharField(max_length=150)
    image = models.FileField(upload_to="book/")
    author = models.CharField(max_length=150)
    detail = models.CharField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    categories = models.ManyToManyField('BookCategory', related_name='books', blank=True)

class BookCategory(models.Model):
    category_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.category_name

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Cart {self.id} for {self.user}'

class CartDetail(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='inactive')

    def __str__(self):
        return f'{self.quantity} of {self.book.title} in Cart {self.cart.id}'

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    order_date = models.DateTimeField(auto_now_add=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=50, default='unpaid')

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
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    image = models.FileField(upload_to="payment/")
    payment_date = models.DateTimeField(auto_now_add=True)
    method = models.CharField(max_length=50)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f'Payment {self.id} for Order {self.order.id}'
    
class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField()
    comment = models.CharField(max_length=500, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Review by {self.user} for {self.book.title}'