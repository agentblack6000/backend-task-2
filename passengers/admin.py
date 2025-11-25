"""
Registers the Passenger, Ticket, Connection, and Line models to define the railway network
For the Station model, some additional functionality:
    View the number of tickets starting/ending at each station, provided the ticket is active
    or in use.
    The list of tickets associated with that station
"""
from django.contrib import admin
from django.db import models
from .models import Station, Passenger, Ticket, Connection, Line

# The register decorator is used here since we have a custom class for the Station-admin interface
@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    """
    Implements a custom Station-admin interface that displays all tickets associated with that
    station provided the ticket is active or in use and the list of tickets associated with that
    station
    """

    # Which columns to show for this model
    list_display = ["name", "ticket_count", "tickets_overview"]

    # When using a callable, a model method, or a ModelAdmin method, you can customize
    # the column’s title by wrapping the callable with admin's display() decorator
    @admin.display(description="Active/In Use Ticket count")
    def ticket_count(self, obj) -> int:
        """
        Returns the ticket count for all tickets that have start/end station as the given station
        (represented by the obj, the instance of the Station), given the ticket status is active or
        in use.
        """

        # By default, filter uses AND operations which isn't always needed.
        # models.Q (QueryExpression )structures a more complex query that can involve OR, NOT,
        # as well as AND operations. Here, it is used to query the tickets which have start/end
        # stations as the given station, and are active or in use
        count = Ticket.objects.filter(
            (models.Q(start_station=obj) | models.Q(destination=obj))
            & (models.Q(status="active") | models.Q(status="in use"))
        ).count()

        return count

    @admin.display(description="Ticket Data")
    def tickets_overview(self, obj) -> str:
        """
        Returns a comma separated list of all tickets connected to this station
        ex:
            "user (Station A to Station B), ..."
        Returns '-' if no tickets exist
        """
        tickets = Ticket.objects.filter(
            models.Q(start_station=obj) | models.Q(destination=obj)
        )

        # Displays - if there are no tickets associated with that station
        if not tickets.exists():
            return "-"

        return ", ".join(
            [
                f"{t.passenger.user.username} ({t.start_station.name} to {t.destination.name})"
                for t in tickets
            ]
        )


# Registers the remaining models:
admin.site.register(Passenger)
admin.site.register(Ticket)
admin.site.register(Connection)
admin.site.register(Line)
