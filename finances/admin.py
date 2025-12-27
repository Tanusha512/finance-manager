# finances/admin.py
from django.contrib import admin
from .models import Category, Transaction

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_income']
    list_filter = ['is_income']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['date', 'category', 'amount', 'user', 'description']
    list_filter = ['date', 'category', 'user']
    search_fields = ['description']
    date_hierarchy = 'date'
