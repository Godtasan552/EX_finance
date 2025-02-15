from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Transaction, Category
from .forms import SignUpForm, TransactionForm, CategoryForm
from django.http import HttpResponse,JsonResponse
from datetime import datetime
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied
from django.db.models import Sum
from django.contrib import messages
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

@login_required 
def dashboard(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('-date', '-id')  # เรียงจากใหม่ไปเก่า
    
    # Handle filters
    filter_type = request.GET.get('filter_type', '')
    filter_category = request.GET.get('filter_category', '')
    filter_date = request.GET.get('filter_date', '')

    if filter_type:
        transactions = transactions.filter(type=filter_type)
    if filter_category:
        transactions = transactions.filter(category__name=filter_category)
    if filter_date:
        try:
            date_filter = datetime.strptime(filter_date, '%Y-%m-%d').date()
            transactions = transactions.filter(date=date_filter)
        except ValueError:
            pass

    categories = Category.objects.all()
    form = TransactionForm()

    context = {
        'transactions': transactions,
        'form': form,
        'categories': categories,
        'filter_type': filter_type,
        'filter_category': filter_category,
        'filter_date': filter_date,
    }
    
    if form.errors:
        context['form_errors'] = form.errors

    return render(request, 'dashboard.html', context)

@login_required
def add_category(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')  # รับค่า ID ของหมวดหมู่ที่ต้องการแก้ไข
        if category_id:
            category = get_object_or_404(Category, id=category_id)
            form = CategoryForm(request.POST, instance=category)
            if form.is_valid():
                form.save()
                messages.success(request, 'Category updated successfully!')
                return redirect('add_category')
        else:
            form = CategoryForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Category added successfully!')
                return redirect('add_category')
    else:
        form = CategoryForm()

    categories = Category.objects.all()  
    return render(request, 'add_category.html', {'form': form, 'categories': categories})

@login_required
def generate_report(request):
    start_date = request.GET.get('start_date', '')
    end_date = request.GET.get('end_date', '')

    transactions = Transaction.objects.filter(user=request.user)

    if start_date and end_date:
        transactions = transactions.filter(date__range=[start_date, end_date])

    total_income = transactions.filter(type='income').aggregate(total=Sum('amount'))['total'] or 0
    total_expense = transactions.filter(type='expense').aggregate(total=Sum('amount'))['total'] or 0
    balance = total_income - total_expense
    
    return render(request, 'generate_report.html', {
        'total_income': total_income,
        'total_expense': total_expense,
        'transactions': transactions,  # ส่ง transactions ไปด้วย
        'start_date': start_date,
        'end_date': end_date,
        'balance': balance,
    })

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


def get_categories(request):
    type_filter = request.GET.get('type', '')
    categories = Category.objects.filter(type=type_filter) if type_filter else Category.objects.all()
    data = {"categories": [{"id": cat.id, "name": cat.name} for cat in categories]}
    return JsonResponse(data)


@login_required
def add_transaction(request):
    categories = Category.objects.all()  # ดึงข้อมูลหมวดหมู่ทั้งหมด
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('dashboard')
    else:
        form = TransactionForm()

    return render(request, 'add_transaction.html', {'form': form, 'categories': categories})
