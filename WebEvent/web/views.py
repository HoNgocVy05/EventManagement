from web.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Event
from django.utils.timezone import make_aware

# Create your views here.
def get_index(request):
    events = Event.objects.all()
    return render(request, 'index.html', {'events': events})
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

@login_required
def add_edit_event(request, event_id=None):
    event = None
    if event_id:
        event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        start_time = request.POST['start_time']
        tickets = request.POST['tickets']
        image = request.FILES.get('image')
        if event:  
            event.name = name
            event.description = description
            event.start_time = start_time
            event.tickets = tickets
            if image:
                event.image = image
        else:
            event = Event.objects.create(
                name=name,
                description=description,
                start_time=start_time,
                tickets=tickets,
                image=image
            )
        event.save()
        return redirect('index')
    return render(request, 'add-edit-event.html', {'event': event})

@login_required
def endevent(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.user.is_staff:
        event.is_ended = True
        event.status = 'Completed'
        event.save()
        messages.success(request, "Sự kiện đã được kết thúc thành công.")
    else:
        messages.error(request, "Bạn không có quyền thực hiện thao tác này.")
    
    return redirect('eventdetail', event_id=event.id)

def eventdetail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    return render(request, 'eventdetail.html', {'event': event})
