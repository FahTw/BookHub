from django import forms
from django.contrib.auth.models import User
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
    