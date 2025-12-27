# finances/urls.py
from django.urls import path
from . import views

app_name = 'finances'

urlpatterns = [
    path('', views.transaction_list, name='transaction_list'),
    path('add/', views.add_transaction, name='add_transaction'),
]
