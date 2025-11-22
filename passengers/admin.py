from django.contrib import admin
from .models import Station, Passenger, Ticket
# Register your models here.

admin.site.register(Station)
admin.site.register(Passenger)
admin.site.register(Ticket)
