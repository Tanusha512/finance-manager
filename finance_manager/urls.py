# finance_manager/urls.py
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from finances import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('finances.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('register/', views.register, name='register'),
]
