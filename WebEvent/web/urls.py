from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import logout

urlpatterns = [
    path('', views.get_index, name='index'),
    path('login/', views.get_login, name='login'),
    path('signup/', views.get_signup, name='signup'),
    path('logout/', views.get_logout, name='logout'),
    path('profile/', views.profile, name='profile'),
]