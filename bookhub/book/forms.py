from django import forms
from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.core.exceptions import ValidationError
 
class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2', 'phone', 'address', 'province', 'postal_code']
        widgets = {"address": forms.Textarea(attrs={'rows': 3})}

    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")

        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("อีเมลถูกใช้งานแล้ว กรุณาใช้อีเมลอื่น")

        return cleaned_data

class UserProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'address', 'phone', 'province', 'postal_code']
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get("email")
        user_id = self.instance.id

        if CustomUser.objects.filter(email=email).exclude(id=user_id).exists():
            raise ValidationError("อีเมลถูกใช้งานแล้ว กรุณาใช้อีเมลอื่น")

        return cleaned_data

class CartForm(ModelForm):
    class Meta:
        model = Cart
        fields = ['user', 'book', 'quantity', 'price', 'total_price', 'status']

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        
        if quantity and quantity <= 0:
            raise ValidationError("จำนวนต้องมากกว่า 0")

        return cleaned_data

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['user', 'cart', 'order_date', 'total_amount', 'status']

    def clean(self):
        cleaned_data = super().clean()
        quantity = cleaned_data.get("quantity")
        
        if quantity and quantity <= 0:
            raise ValidationError("จำนวนต้องมากกว่า 0")

        return cleaned_data

class PaymentForm(ModelForm):
    class Meta:
        model = Payment
        fields = ['order', 'payment_slip', 'payment_date', 'method', 'amount', 'status', 'verified_date']

    def clean(self):
        cleaned_data = super().clean()
        payment_slip = cleaned_data.get("payment_slip")
        method = cleaned_data.get("method")
        amount = cleaned_data.get("amount")

        # Payment slip is not required for cash on delivery
        if method != 'cash' and not payment_slip:
            raise ValidationError("กรุณาอัพโหลดหลักฐานการชำระเงิน")

        if amount and amount <= 0:
            raise ValidationError("จำนวนเงินต้องมากกว่า 0")

        return cleaned_data

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["title", "image", "author", "publisher", "detail", "price", "stock"]

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        stock = cleaned_data.get("stock")

        if price and price <= 0:
            raise ValidationError("ราคาต้องมากกว่า 0")

        if stock and stock < 0:
            raise ValidationError("จำนวนสต็อกต้องเป็นจำนวนเต็มบวก")

        return cleaned_data
