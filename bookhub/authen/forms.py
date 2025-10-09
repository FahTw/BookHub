from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError
class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = [
            'first_name', 
            'last_name', 
            'email', 
            'password'
        ]
    def clean(self):
        cleaned_data = super().clean()
        email = cleaned_data.get('email')
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
        if User.objects.filter(email=email).exists():
            raise ValidationError(
                "Email นี้ถูกใช้งานแล้ว กรุณาใช้อีเมลอื่น"
            )
        if confirm_password != password:
            raise ValidationError(
                "รหัสผ่านไม่ตรงกัน กรุณากรอกใหม่"
            )
        return cleaned_data