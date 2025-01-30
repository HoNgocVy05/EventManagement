from web.models import User
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Event, Ticket
from django.utils.timezone import make_aware
import uuid
from django.core.mail import send_mail

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
            return render(request, 'signup.html')
        
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html')
        
        user = User(username=username, email=email, password=make_password(password))
        user.save()
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
            return render(request, 'login.html')
        if user.check_password(password):
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html')
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
    event.is_ended = True
    event.status = 'Completed'
    event.save()
    return redirect('eventdetail', event_id=event.id)

@login_required
def deleteevent(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Ticket.objects.filter(event=event).delete()
    event.delete()
    return redirect('index')

def eventdetail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    context = {'event': event,}
    return render(request, 'eventdetail.html', {'event': event})

def buyticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        quantity = int(request.POST.get('quantity'))

        if event.tickets < quantity:
            return redirect('buyticket', event_id=event.id)

        event.tickets -= quantity
        event.save()

        tickets = []
        for _ in range(quantity):
            qr_code = str(uuid.uuid4())[:8]
            ticket = Ticket.objects.create(
                event=event,
                user=request.user,
                email=email,
                phone_number=phone_number,
                qr_code=qr_code
            )
            tickets.append(ticket)

        ticket_details = "\n".join([f"Vé: {t.qr_code} - {event.name}" for t in tickets])
        send_mail(
            subject="Xác nhận mua vé",
            message=f"Bạn đã mua {quantity} vé cho sự kiện {event.name}.\nMã QR của bạn:\n{ticket_details}",
            from_email="vyhn5306@ut.edu.vn",
            recipient_list=[email]
        )
        return redirect('yourtickets')
    return render(request, 'buytickets.html', {'event': event})

def yourtickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'yourticket.html', {'tickets': tickets})