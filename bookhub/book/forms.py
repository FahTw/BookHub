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
        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")
        postal_code = cleaned_data.get("postal_code")

        if phone and not phone.isdigit():
            self.add_error('phone', "เบอร์โทรศัพท์ต้องเป็นตัวเลขเท่านั้น")

        if email and CustomUser.objects.filter(email=email).exists():
            self.add_error('email', "อีเมลถูกใช้งานแล้ว กรุณาใช้อีเมลอื่น")
        
        if postal_code and not postal_code.isdigit():
            self.add_error('postal_code', "รหัสไปรษณีย์ต้องเป็นตัวเลขเท่านั้น")

        return cleaned_data

class UserProfileForm(ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'address', 'phone', 'province', 'postal_code']
    
    # ตรวจสอบความถูกต้องของข้อมูล
    def clean(self):
        cleaned_data = super().clean()
        phone = cleaned_data.get("phone")
        email = cleaned_data.get("email")
        postal_code = cleaned_data.get("postal_code")
        
        # ดึง user_id 
        user_id = self.instance.id

        if phone and not phone.isdigit():
            self.add_error('phone', "เบอร์โทรศัพท์ต้องเป็นตัวเลขเท่านั้น")
        
        # ตรวจสอบ email ว่ามีการใช้งานแล้วหรือไม่ โดยยกเว้นตเจ้าของ id นั้นๆ
        if email and CustomUser.objects.filter(email=email).exclude(id=user_id).exists():
            self.add_error('email', "อีเมลถูกใช้งานแล้ว กรุณาใช้อีเมลอื่น")
        
        if postal_code and not postal_code.isdigit():
            self.add_error('postal_code', "รหัสไปรษณีย์ต้องเป็นตัวเลขเท่านั้น")

        return cleaned_data

class BookForm(ModelForm):
    class Meta:
        model = Book
        fields = ["title", "image", "author", "publisher", "publication_date", "pages", "language", "detail", "price", "stock", "categories"]
        widgets = {
            'categories': forms.CheckboxSelectMultiple(),
            'detail': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        price = cleaned_data.get("price")
        stock = cleaned_data.get("stock")

        if price and price <= 0:
            raise ValidationError("ราคาต้องมากกว่า 0")

        if stock and stock < 0:
            raise ValidationError("จำนวนสต็อกต้องเป็นจำนวนเต็มบวก")

        return cleaned_data

class BookCategoryForm(ModelForm):
    class Meta:
        model = BookCategory
        fields = ["category_name", "description"]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean(self):
        cleaned_data = super().clean()
        category_name = cleaned_data.get("category_name")

        if not self.instance.pk and BookCategory.objects.filter(category_name=category_name).exists():
            raise ValidationError("ประเภทหนังสือนี้มีอยู่แล้ว")

        return cleaned_data

class ReviewForm(ModelForm):
    class Meta:
        model = Review
        fields = ['comment', 'rating']
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 4}),
            'rating': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }
