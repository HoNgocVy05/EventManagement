from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username
User = get_user_model()

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    tickets = models.PositiveIntegerField()
    curr_tickets = models.PositiveIntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    is_ended = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    qr_code = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Vé của {self.user.username} - {self.event.name}"
    
class Sponsor (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username