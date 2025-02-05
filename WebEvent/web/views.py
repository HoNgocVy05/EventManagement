from web.models import User
from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from django.contrib.auth.hashers import make_password
from django.contrib.auth import get_user_model
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from .models import Event, Ticket, Sponsor
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
            return render(request, 'signup.html', {"error_message": "Mật khẩu không khớp!"})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {"error_message": "Email đã tồn tại!"})
        
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
            return render(request, 'login.html', {"error_message": "Email không tồn tại!"})
        
        if user.check_password(password):
            login(request, user)
            return redirect('index')
        else:
            return render(request, 'login.html', {"error_message": "Mật khẩu không chính xác!"})
    
    return render(request, 'login.html')


def get_logout(request):
    logout(request)
    return redirect('index')

def profile(request):
    user = request.user
    return render(request, 'profile.html', {'user': user})

def add_edit_event(request, event_id=None):
    event = None
    if event_id:
        event = get_object_or_404(Event, id=event_id)
    else:
        is_new_event = True 
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
        if is_new_event:
            promotionemail(event)
        return redirect('index')
    return render(request, 'add-edit-event.html', {'event': event})

def promotionemail(event):
    subject = "Sự kiện mới trên EVENTHUB"
    from_email = "hna.191081@gmail.com"
    
    users = User.objects.all().values_list('email', flat=True)  
    recipient_list = list(users)

    if recipient_list:  
        mailcontent = format_html(f"""
            <html>
            <body>
                <h2 style="color: #2c3e50;">{event.name}</h2>
                <p><strong>Thời gian:</strong> {event.start_time}</p>
                <p><strong>Giá vé:</strong> {'Miễn phí' if event.price == 0 else f"{event.price} VNĐ"}</p>
                <p>Có thể bạn sẽ quan tâm đến sự kiện này.</p>
                <p><a href="http://127.0.0.1:8000/event/{event.id}" 
                      style="background-color: #333333; color: white; padding: 10px 15px; text-decoration: none; border-radius: 5px;">
                      Xem Chi Tiết Sự Kiện Tại Đây
                   </a></p>
                <p style="margin-top:20px; color:#666;">Trân trọng,<br>EVENTHUB</p>
            </body>
            </html>
        """)

        email_message = EmailMultiAlternatives(subject, "Sự kiện mới!", from_email, bcc=recipient_list)
        email_message.attach_alternative(mailcontent, "text/html")
        email_message.send()

def endevent(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    event.is_ended = True
    event.status = 'Completed'
    Ticket.objects.filter(event=event).delete()
    event.save()
    return redirect('eventdetail', event_id=event.id)

def deleteevent(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    Ticket.objects.filter(event=event).delete()
    event.delete()
    return redirect('index')

def eventdetail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    out_of_tickets = event.tickets <= 0
    context = {'event': event,}
    return render(request, 'eventdetail.html', {'event': event, 'out_of_tickets': out_of_tickets})

def buyticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    if request.method == 'POST':
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        quantity = int(request.POST.get('quantity'))
        total_price = event.price * quantity
        if event.curr_tickets < quantity:
            return redirect('buyticket', event_id=event.id)
        event.curr_tickets -= quantity
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

def eventmanagement(request):
    is_sponsor = Sponsor.objects.filter(user=request.user).exists()
    if is_sponsor:
        events = Event.objects.filter(event_sponsors__user=request.user)
    else:
        events = Event.objects.all()
    event_data = []
    for event in events:
        sponsors = event.sponsors.all()
        tickets_sold = Ticket.objects.filter(event=event).count()
        event_data.append({
            "event": event,
            "sponsors": event.event_sponsors.all(),
            "total_tickets": event.tickets,
            "tickets_sold": tickets_sold,
            "remaining_tickets": max(event.tickets - tickets_sold, 0),
            "ticket_list": Ticket.objects.filter(event=event),
        })
    return render(request, "eventmanagement.html", {"event_data": event_data})

def addsponsor(request, event_id):
    event = get_object_or_404(Event, id=event_id)  
    existing_sponsors = Sponsor.objects.filter(event=event).values_list("user", flat=True)   
    available_sponsors = User.objects.filter(sponsor__isnull=False).exclude(id__in=existing_sponsors)
    if request.method == "POST":
        sponsor_email = request.POST.get("sponsor_email")
        name = request.POST.get("name")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_psw = request.POST.get("confirm_password")
        if sponsor_email:
            sponsor_user = User.objects.filter(email=sponsor_email).first()
            if not sponsor_user:
                return render(request, "addsponsor.html", {
                    "event": event,
                    "error_message": "Email không tồn tại trong hệ thống!"
                })     
            if Sponsor.objects.filter(user=sponsor_user, event=event).exists():
                return render(request, "addsponsor.html", {"event": event, "error_message": "Tài khoản này đã tồn tại trong danh sách nhà tại trợ cho sự kiện này!"})

            Sponsor.objects.create(user=sponsor_user, event=event)
            send_sponsor_email(sponsor_user, event, existing=True)

        else:
            if password != confirm_psw:
                return render(request, "addsponsor.html", {"event": event, "error_message": "Mật khẩu không khớp!"})
            if User.objects.filter(email=email).exists():
                return render(request, "addsponsor.html", {"event": event, "error_message": "Email đã tồn tại!"})
            if User.objects.filter(username=name).exists():
                return render(request, "addsponsor.html", {"event": event, "error_message": "Tên đã tồn tại!"})
            sponsor_user = User.objects.create(
                username=name,
                email=email,
                password=make_password(password)
            )
            Sponsor.objects.create(user=sponsor_user, event=event)
            send_sponsor_email(sponsor_user, event, password)
        return redirect("eventdetail", event_id=event.id)
    return render(request, "addsponsor.html", {"event": event, "available_sponsors": available_sponsors})

def send_sponsor_email(user, event, password=None, existing=False):
    subject = "Bạn đã trở thành nhà tài trợ sự kiện tại EVENTHUB"
    from_email = "hna.191081@gmail.com"
    to_email = [user.email]
    if existing:
        mailcontent = format_html(f"""
            <html>
            <body>
                <h2 style="color: #2c3e50;">Kính chào {user.username},</h2>
                <p>Bạn đã được thêm làm nhà tài trợ cho sự kiện <strong>{event.name}</strong>.</p>
                <p>Bạn có thể đăng nhập vào hệ thống bằng tài khoản chúng tôi cung cấp trước đó để xem báo cáo sự kiện. <br>Nếu quên mật khẩu, hãy liên hệ qua <strong>hna.191081@gmail.com<strong> để được hỗ trợ</p>
                <p style="margin-top:20px; color:#666;">Trân trọng,<br>Ban tổ chức sự kiện</p>
            </body>
            </html>
        """)
    else:
        mailcontent = format_html(f"""
            <html>
            <body>
                <h2 style="color: #2c3e50;">Kính chào {user.username},</h2>
                <p>Bạn đã được tạo tài khoản và trở thành nhà tài trợ cho sự kiện <strong>{event.name}</strong>.</p>
                <p><strong>Email:</strong> {user.email}</p>
                <p><strong>Mật khẩu:</strong> {password}</p>
                <p>Bạn có thể đăng nhập vào hệ thống để xem báo cáo sự kiện.</p>
                <p style="margin-top:20px; color:#666;">Trân trọng,<br>Ban tổ chức sự kiện</p>
            </body>
            </html>
        """)
    email_message = EmailMultiAlternatives(subject, "Thông báo tài trợ sự kiện", from_email, to_email)
    email_message.attach_alternative(mailcontent, "text/html")
    email_message.send()

def checksponsor(request):
    email = request.GET.get("email", "").strip()
    try:
        sponsor = User.objects.get(email=email)
        return JsonResponse({"exists": True, "name": sponsor.username})
    except User.DoesNotExist:
        return JsonResponse({"exists": False})