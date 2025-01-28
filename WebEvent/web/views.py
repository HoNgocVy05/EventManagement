from web.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required

# Create your views here.
def get_index(request):
    return render(request, 'index.html')
    if request.method == "POST":
        username = request.POST['username']

def get_signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_psw = request.POST['confirm_psw']
        
        if password != confirm_psw:
            return render(request, 'signup.html', {'error': 'Mật khẩu không khớp!'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email đã tồn tại!'})
        
        user = User(username=username, email=email, password=make_password(password))
        user.save()
        messages.success(request, 'Đăng ký thành công! Hãy đăng nhập.')
        return redirect('login')
    return render(request, 'signup.html')

def get_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        User = get_user_model()
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return render(request, 'login.html', {'error': 'Email không tồn tại'})
        if user.check_password(password):
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {'error': 'Mật khẩu hoặc email không đúng'})
    return render(request, 'login.html')

def get_logout(request):
    logout(request)
    return redirect('index')

@login_required
def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})