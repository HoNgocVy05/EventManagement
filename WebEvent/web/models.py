from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(unique=True)
    def __str__(self):
        return self.username
    def is_sponsor(self):
        return hasattr(self, "sponsor")
    
User = get_user_model()

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    start_time = models.DateTimeField()
    tickets = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=3, default=0)
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    is_ended = models.BooleanField(default=False)
    sponsors = models.ManyToManyField('Sponsor', related_name="events")
    ticket_sold = models.IntegerField(default=0)
    curr_ticket = models.IntegerField(default=0)
    
    def __str__(self):
        return self.name
    
class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField()
    phone_number = models.CharField(max_length=10)
    qr_code = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    is_guest = models.BooleanField(default=False)

    def __str__(self):
        return f"Vé của {self.user.username} - {self.event.name}"
    
class Sponsor (models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="event_sponsors")

    class Meta:
        unique_together = ('user', 'event')

    def __str__(self):
        return f"{self.user.username} - {self.event.name}"
    
class Attended(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    email = models.EmailField()

    class Meta:
        unique_together = ('event', 'email') 
    def __str__(self):
        return self.email

class Survey(models.Model):
    event = models.ForeignKey('Event', on_delete=models.CASCADE, related_name="surveys")
    email = models.EmailField()
    rating_1 = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True)
    rating_2 = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True)
    rating_3 = models.PositiveIntegerField(choices=[(i, str(i)) for i in range(1, 6)], null=True)
    feedback = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Survey for {self.event.name} by {self.email}"
    
class Guest(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="guests")
    name = models.CharField(max_length=255)
    email = models.EmailField()

    def __str__(self):
        return f"{self.name} - {self.email}"