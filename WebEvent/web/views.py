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
from django.core.mail import EmailMultiAlternatives
from django.utils.html import format_html
from django.http import JsonResponse

# Create your views here.
def get_index(request):
    events = Event.objects.all()
    if request.method == "POST":
        username = request.POST['username']
    events = Event.objects.all().order_by('is_ended', '-start_time')
    return render(request, 'index.html', {'events': events})

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
        image = request.FILES.get('image')
        tickets = request.POST.get('tickets', 0)
        price = request.POST.get('price', 0)
        if event:  
            event.name = name
            event.description = description
            event.start_time = start_time
            event.tickets = tickets
            event.price = price
            if image:
                event.image = image
        else:
            event = Event.objects.create(
                name=name,
                description=description,
                start_time=start_time,
                tickets=tickets,
                image=image,
                price=price
            )
        event.save()
        return redirect('index')
    return render(request, 'add-edit-event.html', {'event': event})

@login_required
def endevent(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.is_ended = True
    event.status = 'Completed'
    Ticket.objects.filter(event=event).delete()
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
        total_price = event.price * quantity

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

        ticket_details = "".join([
            f"<p><strong>Vé:</strong> {t.qr_code}</p>"
            f'<img src="https://api.qrserver.com/v1/create-qr-code/?size=150x150&data={t.qr_code}" alt="QR Code">'
            for t in tickets
        ])

        subject = "Xác nhận mua vé"
        from_email = "hna.191081@gmail.com"
        to_email = [email]

        mailcontent = format_html(f"""
            <html>
            <body>
                <h2 style="color: #2c3e50;">Xác nhận mua vé</h2>
                <p>Chào bạn,</p>
                <p>Bạn đã mua <strong>{quantity}</strong> vé cho sự kiện <strong>{event.name}</strong>.</p>
                <p><strong>Thời gian sự kiện:</strong> {event.start_time.strftime("%d/%m/%Y %H:%M")}</p>
                <p>Cảm ơn bạn đã quan tâm đến sự kiện của chúng tôi!</p>
                <h3>Chi tiết vé:</h3>
                {ticket_details}
                <p style="margin-top:20px; color:#666;">Trân trọng,<br>Ban tổ chức sự kiện</p>
            </body>
            </html>
        """)

        email_message = EmailMultiAlternatives(subject, "Bạn đã mua vé thành công.", from_email, to_email)
        email_message.attach_alternative(mailcontent, "text/html")
        email_message.send()

        return redirect('yourtickets')
    
    return render(request, 'buytickets.html', {'event': event})

def yourtickets(request):
    tickets = Ticket.objects.filter(user=request.user)
    return render(request, 'yourticket.html', {'tickets': tickets})

def evenlist(request):
    events = Event.objects.all()
    events = Event.objects.all().order_by('is_ended', '-start_time')
    return render(request, 'list.html', {'events': events})

def introduction(request):
    return render(request, 'introduction.html')

def search_events(request):
    query = request.GET.get('q', '').strip()
    
    if request.GET.get('ajax'):
        events = Event.objects.filter(name__icontains=query)[:5] if query else []
        data = [{"id": event.id, "name": event.name, "description": event.description} for event in events]
        return JsonResponse(data, safe=False)

    events = Event.objects.filter(name__icontains=query) if query else []
    return render(request, 'eventresult.html', {'events': events, 'query': query})