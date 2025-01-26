from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_index, name='index'),
    path('login/', views.get_login, name='login'),
    path('signup/', views.get_signup, name='signup'),
    path('signup_view/', views.signup_view, name='signup_view'),
    path('login_view/', views.login_view, name='login_view'),
]