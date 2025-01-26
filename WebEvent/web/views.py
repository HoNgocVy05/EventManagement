from django.shortcuts import render

# Create your views here.
def get_index(request):
    return render(request, 'index.html')

def get_login(request):
    return render(request, 'login.html')

def get_signup(request):
    return render(request, 'signup.html')