from django import forms
from django.contrib.auth.models import User
from .models import Book, Review
from django.core.exceptions import ValidationError

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-input'}),
            'last_name': forms.TextInput(attrs={'class': 'form-input'}),
            'email': forms.EmailInput(attrs={'class': 'form-input'}),
            # 'profile.address': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 4}),
        }

    def clean_email(self):
        
        email = self.cleaned_data.get('email')
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
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

