
from .models import Category
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction
from django.core.exceptions import ValidationError

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username

    def clean_password(self):
        password = self.cleaned_data.get('password')
        # ตรวจสอบความยาวของรหัสผ่าน (ต้องมีอย่างน้อย 8 ตัวอักษร)
        if len(password) < 8:
            raise ValidationError("Password must be at least 8 characters long.")
        # ตรวจสอบให้แน่ใจว่ามีตัวเลขอย่างน้อย 1 ตัวในรหัสผ่าน
        if not any(char.isdigit() for char in password):
            raise ValidationError("Password must contain at least one digit.")
        # ตรวจสอบให้มีตัวอักษรพิเศษในรหัสผ่าน
        if not any(char in "!@#$%^&*()" for char in password):
            raise ValidationError("Password must contain at least one special character: !@#$%^&*()")
        return password

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'type', 'description', 'category']
    
    # เพิ่มตัวเลือก category ให้ผู้ใช้เลือกจากฐานข้อมูล
    category = forms.ModelChoiceField(queryset=Category.objects.all(), empty_label="Select Category")



class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description']  # กำหนดฟิลด์ที่ต้องการในฟอร์ม

class TransactionFilterForm(forms.Form):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)
    category = forms.CharField(required=False)