from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_index, name='index'),
    path('login/', views.get_login, name='login'),
]