
from .models import Category,Transaction
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
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
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),  # ปรับให้ description ขนาดเท่ากัน
        }

    # เพิ่มตัวเลือก category ให้ผู้ใช้เลือกจากฐานข้อมูล
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select Category",
        widget=forms.Select(attrs={'class': 'form-control'})
    )


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'description', 'type']


class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['amount', 'date', 'type', 'description', 'category']
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].queryset = Category.objects.none()  # เริ่มต้นเป็นว่าง

        if 'type' in self.data:
            try:
                category_type = self.data.get('type')
                self.fields['category'].queryset = Category.objects.filter(type=category_type)
            except (ValueError, TypeError):
                pass
