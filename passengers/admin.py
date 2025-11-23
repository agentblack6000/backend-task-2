from django.contrib import admin
from .models import Station, Passenger, Ticket, Connection, Line
# Register your models here.

admin.site.register(Station)
admin.site.register(Passenger)
admin.site.register(Ticket)
admin.site.register(Connection)
admin.site.register(Line)