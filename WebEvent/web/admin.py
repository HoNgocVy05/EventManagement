from django.contrib import admin
from web.models import User
from .models import User, Event, Ticket, Sponsor, Survey, Attended

# Register your models here.
admin.site.register(User)
admin.site.register(Event)
admin.site.register(Ticket)
admin.site.register(Sponsor)
admin.site.register(Survey)
admin.site.register(Attended)