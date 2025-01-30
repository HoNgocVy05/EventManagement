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
    image = models.ImageField(upload_to='events/', null=True, blank=True)
    is_ended = models.BooleanField(default=False)

    def __str__(self):
        return self.name