from django.contrib import admin
from web.models import User
from .models import User, Event, Ticket

# Register your models here.
admin.site.register(User)
admin.site.register(Event)
