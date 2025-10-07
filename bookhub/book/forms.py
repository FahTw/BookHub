from django import forms
from .models import Payment, Order

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
