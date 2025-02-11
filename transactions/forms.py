
from .models import Category
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Transaction


class SignUpForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password', 'email']
    
    password = forms.CharField(widget=forms.PasswordInput)
    email = forms.EmailField()

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Username already exists.")
        return username
  # กำหนดขีดจำกัดเป็น 50 ตัวอักษร

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
