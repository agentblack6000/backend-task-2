from django.contrib import admin
from django.db import models
from django.utils.html import format_html
from .models import Station, Passenger, Ticket, Connection, Line
# Register your models here.

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    list_display = ["name", "ticket_count", "tickets_list"]

    def ticket_count(self, obj):
        """Returns the total number of tickets starting or ending at this station"""
        count = Ticket.objects.filter(
            models.Q(start_station=obj) | models.Q(destination=obj)
        ).count()
        return count
    ticket_count.short_description = "Number of Tickets"

    def tickets_list(self, obj):
        """Returns a bullet point list of tickets"""
        tickets = Ticket.objects.filter(
            models.Q(start_station=obj) | models.Q(destination=obj)
        )
        if not tickets.exists():
            return "-"
        
        return ", ".join([
            f"{t.passenger.user.username} ({t.start_station.name} to {t.destination.name})"
            for t in tickets
        ])
    tickets_list.short_description = "Ticket Data"


admin.site.register(Passenger)
admin.site.register(Ticket)
admin.site.register(Connection)
admin.site.register(Line)