# finances/views.py
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from .models import Transaction, Category
from .forms import TransactionForm
from datetime import date, timedelta
from collections import defaultdict
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib import messages

@login_required
def transaction_list(request):
    transactions = Transaction.objects.filter(user=request.user).order_by('date')
    
    income = sum(t.amount for t in transactions if t.category.is_income)
    expense = sum(t.amount for t in transactions if not t.category.is_income)
    balance = income - expense

    # 📊 Подготовка данных для графика
    labels = []
    balance_data = []
    current_balance = 0.0

    for t in transactions:
        if t.category.is_income:
            current_balance += float(t.amount)
        else:
            current_balance -= float(t.amount)
        labels.append(t.date.strftime('%d.%m.%Y'))
        balance_data.append(round(current_balance, 2))

    # Если нет транзакций — одна точка "Сегодня"
    if not labels:
        labels = ['Сегодня']
        balance_data = [0.0]

    chart_data = {
        'labels': labels,
        'balance': balance_data,
        'income': float(income),
        'expense': float(expense),
    }

    return render(request, 'finances/transaction_list.html', {
        'transactions': transactions.order_by('-date'),
        'income': income,
        'expense': expense,
        'balance': balance,
        'chart_data': chart_data,
    })

@login_required
def add_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.user = request.user
            transaction.save()
            return redirect('finances:transaction_list')
    else:
        form = TransactionForm()
    
    return render(request, 'finances/add_transaction.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'registration/profile.html', {'user': request.user})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # ← создаёт пользователя
            username = form.cleaned_data.get('username')
            messages.success(request, f'Аккаунт {username} создан! Можете войти.')
            return redirect('login')  # ← перенаправляет на /accounts/login/
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})
