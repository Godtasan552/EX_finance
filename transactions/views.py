from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category
from .forms import SignUpForm, TransactionForm, CategoryForm
from django.http import HttpResponse
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied

def home(request):
    return render(request, 'home.html')


# Register
def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
        else:
            return render(request, 'register.html', {'form': form, 'error': 'Registration failed'})
    else:
        form = SignUpForm()
    return render(request, 'register.html', {'form': form})

# Login
def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('dashboard')
        else:
            # แจ้งเตือนกรณีที่ไม่พบผู้ใช้
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    return render(request, 'login.html')

# Logout
def user_logout(request):
    logout(request)
    return redirect('home')

# Dashboard
# Dashboard
# Dashboard
@login_required
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user)
    
    # Filter transactions based on date, category, or type (income/expense)
    filter_type = request.GET.get('filter_type', '')
    filter_category = request.GET.get('filter_category', '')
    filter_date = request.GET.get('filter_date', '')

    # ตรวจสอบค่า filter_type และ filter_category ว่ามีการกรองหรือไม่
    if filter_type:
        transactions = transactions.filter(type=filter_type)
    if filter_category:
        transactions = transactions.filter(category__name=filter_category)

    # ตรวจสอบ filter_date หากมีการกรองวันที่
    if filter_date:
        try:
            date_filter = datetime.strptime(filter_date, '%Y-%m-%d')
            transactions = transactions.filter(date__date=date_filter.date())
        except ValueError:
            return render(request, 'dashboard.html', {
                'error': 'Invalid date format. Please use YYYY-MM-DD.',
                'transactions': transactions
            })

    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()
    
    categories = Category.objects.all()

    return render(request, 'dashboard.html', {'transactions': transactions, 'form': form, 'categories': categories})


# Add Category
# Add Category
@login_required
def add_category(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category_name = form.cleaned_data['name']
            # ตรวจสอบ category ที่ชื่อซ้ำ
            if Category.objects.filter(name=category_name).exists():
                return render(request, 'add_category.html', {'form': form, 'error': 'Category already exists'})
            form.save()
            return redirect('dashboard')
    else:
        form = CategoryForm()
    return render(request, 'add_category.html', {'form': form})

# Generate Reports
@login_required
def generate_report(request):
    # Example: Generate monthly report
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    transactions = Transaction.objects.filter(user=request.user)

    if start_date and end_date:
        transactions = transactions.filter(date__range=[start_date, end_date])

    # ประมวลผลข้อมูลเชิงสถิติเพื่อสร้างรายงาน (เช่น การรวมยอดรายรับและรายจ่าย)
    total_income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0

    # คุณสามารถสร้างรายงานในรูปแบบ PDF หรือ Excel ได้ที่นี่
    return render(request, 'report.html', {'total_income': total_income, 'total_expense': total_expense})

# View/Update/Delete Transactions
@login_required
def transaction_edit(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id, user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transaction_edit.html', {'form': form, 'transaction': transaction})

from django.shortcuts import get_object_or_404

@login_required
def transaction_delete(request, transaction_id):
    transaction = get_object_or_404(Transaction, id=transaction_id)
    transaction.delete()
    return redirect('dashboard')

@login_required
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    
    # ตรวจสอบว่าหมวดหมู่นี้มีการใช้งานใน Transactions หรือไม่
    if category.transactions.exists():
        return render(request, 'dashboard.html', {'error': 'This category is in use and cannot be deleted.'})
    
    category.delete()
    return redirect('dashboard')

