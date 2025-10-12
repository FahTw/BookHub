from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'first_name', 'last_name', 'email', 'phone', 
            'address', 'province', 'postal_code', 'password1', 'password2'
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError("อีเมลถูกใช้งานแล้ว กรุณาใช้อีเมลอื่น")
        return email


# class RegisterForm(forms.ModelForm):
#     confirm_password = forms.CharField()
#     class Meta:
#         model = User
#         fields = [
#             'first_name', 
#             'last_name', 
#             'email', 
#             'password',
#         ]
#     def clean(self):
#         cleaned_data = super().clean()
#         email = cleaned_data.get('email')
#         password = cleaned_data.get('password')
#         confirm_password = cleaned_data.get('confirm_password')
#         if User.objects.filter(email=email).exists():
#             raise ValidationError(
#                 "Email นี้ถูกใช้งานแล้ว กรุณาใช้อีเมลอื่น"
#             )
#         if confirm_password != password:
#             raise ValidationError(
#                 "รหัสผ่านไม่ตรงกัน กรุณากรอกใหม่"
#             )
#         return cleaned_data

class ProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            'address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise ValidationError("This email is already in use.")
        return email

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating', 'user']
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'rating': forms.NumberInput(attrs={'class': 'form-input', 'min': 1, 'max': 5}),
        }

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['method', 'amount', 'image']
        
    method = forms.ChoiceField(
        choices=[
            ('qr_code', 'QR Code Payment'),
            ('bank_transfer', 'Bank Transfer'),
        ],
        widget=forms.RadioSelect(attrs={
            'class': 'payment-method-radio'
        }),
        label='วิธีการชำระเงิน',
        initial='qr_code'
    )
    
    amount = forms.DecimalField(
        widget=forms.NumberInput(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-orange-500',
            'placeholder': '0.00',
            'readonly': True
        }),
        label='จำนวนเงินที่ชำระ',
        help_text='จำนวนเงินจะถูกกำหนดอัตโนมัติตามยอดสั่งซื้อ'
    )
    
    image = forms.FileField(
        widget=forms.ClearableFileInput(attrs={
            'class': 'hidden',
            'id': 'payment-proof',
            'accept': 'image/*,.pdf',
            'onchange': 'handleFileSelect(this)'
        }),
        label='หลักฐานการชำระเงิน',
        help_text='อัพโหลดสลิปการโอนเงิน หรือหลักฐานการชำระเงิน (รองรับ JPG, PNG, PDF)',
        required=False
    )

    def clean_amount(self):
        amount = self.cleaned_data['amount']
        if self.order and amount != self.order.total_amount:
            raise forms.ValidationError('จำนวนเงินไม่ตรงกับยอดสั่งซื้อ')
        return amount

    def clean_image(self):
        image = self.cleaned_data.get('image')
        if image:
            # Check file size (max 5MB)
            if image.size > 5 * 1024 * 1024:
                raise forms.ValidationError('ขนาดไฟล์ต้องไม่เกิน 5 MB')
            
            # Check file extension
            allowed_extensions = ['.jpg', '.jpeg', '.png', '.pdf']
            file_extension = image.name.lower().split('.')[-1]
            if f'.{file_extension}' not in allowed_extensions:
                raise forms.ValidationError('รองรับเฉพาะไฟล์ JPG, PNG, และ PDF เท่านั้น')
        
        return image

class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        fields = ['status']
        
    status = forms.ChoiceField(
        choices=[
            ('unpaid', 'รอการชำระเงิน'),
            ('paid', 'ชำระเงินแล้ว'),
            ('processing', 'กำลังเตรียมสินค้า'),
            ('shipped', 'จัดส่งแล้ว'),
            ('delivered', 'ส่งมอบแล้ว'),
            ('cancelled', 'ยกเลิกแล้ว'),
        ],
        widget=forms.Select(attrs={
            'class': 'w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:border-orange-500'
        }),
        label='สถานะคำสั่งซื้อ'
    )

class ManageBookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = [
            'title', 'image', 'author', 'detail', 'price', 'stock', 'categories'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-input'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-input'}),
            'author': forms.TextInput(attrs={'class': 'form-input'}),
            'detail': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
            'price': forms.NumberInput(attrs={'class': 'form-input', 'step': '0.01'}),
            'stock': forms.NumberInput(attrs={'class': 'form-input', 'min': 0}),
            'categories': forms.SelectMultiple(attrs={'class': 'form-multiselect'}),
        }
    def clean_price(self):     
        price = self.cleaned_data.get('price')
        if price <= 0:
            raise forms.ValidationError("ราคาต้องมากกว่า 0")
        return price
    
    def clean_stock(self):
        stock = self.cleaned_data.get('stock')
        if stock < 0:
            raise forms.ValidationError("Stock ต้องเป็นจำนวนเต็มบวก")
        return stock
