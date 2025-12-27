# finances/models.py
from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Category(models.Model):
    name = models.CharField("Название", max_length=100)
    is_income = models.BooleanField("Доход", default=False, 
        help_text="Отметьте, если это категория дохода (иначе — расход)")

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"
        ordering = ['is_income', 'name']

    def __str__(self):
        return f"{'🟢' if self.is_income else '🔴'} {self.name}"

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, verbose_name="Категория")
    amount = models.DecimalField("Сумма", max_digits=10, decimal_places=2)
    description = models.CharField("Описание", max_length=255, blank=True)
    date = models.DateField("Дата", auto_now_add=True)

    class Meta:
        verbose_name = "Транзакция"
        verbose_name_plural = "Транзакции"
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} — {self.category} | {self.amount} ₽"

    def get_absolute_url(self):
        return reverse('finances:transaction_list')
