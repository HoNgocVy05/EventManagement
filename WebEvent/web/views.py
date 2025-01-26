from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login

# Create your views here.
def get_index(request):
    return render(request, 'index.html')

def get_login(request):
    return render(request, 'login.html')

def get_signup(request):
    return render(request, 'signup.html')

def signup_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Tên người dùng đã tồn tại'})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email đã tồn tại'})
        
        if password != request.POST['confirm_psw']:
            return render(request, 'signup.html', {'error': 'Mật khẩu không khớp'})


        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()

        return redirect('login')
    return render(request, 'signup.html')

def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')