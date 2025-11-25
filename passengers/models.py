"""
Implementation of the models used to make the metroapp
The db module is to implement the models
The User is for Django's authentication
The utils and datetime module are needed for OTP validation
The pathfinder module finds the shortest path, needed for calculating the price

The kinds of relationships between models are:
one-to-one: models.OneToOneField(), or one instance of this model can be linked to one instance of the model
specified in the OneToOneField(), and vice-versa
many-to-one: models.ForeignKey(), or many instances of this model can be linked to one instance of the model
specified in the ForeignKey
many-to-many: models.ManyToManyField(), or many instances of this model can be linked to many instances of the
model specified in the ManyToManyField
"""
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from passengers.breadth_first_search import shortest_path

# OTP expiry limit in minutes
EXPIRYLIMIT = 10
# OTP length is 6 digits
OTP_LENGTH = 6

class Passenger(models.Model):
    """
    Defines the Passenger model. Stores the bank balance as a DecimalField, to perform accurate
    operations involving floating point numbers. 
    
    A one to one relationship is define between a User and a Passenger, i.e each User has atmost one 
    Passenger and each Passenger has atmost one User. On deletion, the models.CASCADE deletes the User 
    if the Passenger is deleted.
    """

    bank_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        """Useful for the admin interface"""
        return self.user.username


class Station(models.Model):
    """ 
    Defines the Station model, stores the name of the Station in a CharField.
    """

    name = models.CharField(max_length=100)

    def __str__(self):
        """Useful for the admin interface"""
        return self.name


class Ticket(models.Model):
    """ 
    Defines the Ticket model. The cost of each tickt is dynamically calculated based on the 
    start and end stations. The status field is confined to STATUS_CHOICES:
        active: Purchased online
        in use: Scanned at the incoming station, or purchased offline via the admin interface
        expired: Scanned at the outgoing station, marks journey completed
        pending: Status before confirmation, changed to active after payment.

    models.CASCADE is used, i.e if the related Passenger or Station is deleted, all tickets
    related to them should be deleted.
    The relationships at play:
        ForeignKey(Passenger, ...): i.e many tickets can be linked to one Passenger
        ForeignKey(Station, ...): i.e many tickets can be linked to one Station
    """

    # The first value in the tuple is the value stored in the database, the second value is the 
    # human-readable label (for use in forms/admin page)
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in use", "In Use"),
        ("active", "Active"),
        ("expired", "Expired"),
    ]

    # The related name allows for reverse lookups, i.e passenger.tickets.all() will get all tickets
    # for this passenger (Passenger model).
    passenger = models.ForeignKey(
        Passenger, on_delete=models.CASCADE, related_name="tickets"
    )
    start_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="start_station"
    )
    destination = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="destination_station"
    )

    # The cost is dynamically calculated already, it shouldn't be editable
    cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)

    # The status of a newly purchased ticket should be pending
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def calculate_cost(self, start_station, destination_station):
        """
        Uses the algorithm in pathfinder to calculate the cost of the path that takes
        the least distance.
        """
        try:
            cost, distance, stations_crossed = shortest_path(
                start_station, destination_station
            )
        except ValueError:
            return -1

        return cost

    def save(self, *args, **kwargs):
        """ 
        Sets the dynamically calculated cost, and then saves to the database.
        The parent's save method, i.e super().save() is used here for convenience, in the forms we
        were dealing with multiple models (Passenger + User), so the create() was used there which
        internally calls the save(). 
        """
        self.cost = self.calculate_cost(self.start_station, self.destination)
        super().save(*args, **kwargs)

    # Useful for the admin interface
    def __str__(self):
        return f"{self.passenger.user.username}, {self.start_station.name} to {self.destination.name}"


class Line(models.Model):
    """ 
    Defines the Line model. When calculating the shortest path between 2 stations, the is_active is used
    to check if the Line is operational. Admins can mark lines as active or disabled in the admin interface.
    """

    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        """Useful for the admin interface."""
        status = "active" if self.is_active else "disabled"
        return f"{self.name}, ({status})"


class Connection(models.Model):
    """
    Implements the Connection, or the implementation of the actual railway tracks between
    the Stations.
    Each Connection is part of a Line, has a start and destination, stores the distance, travel time,
    and cost. The distance is used in the pathfinding algorithm, provided the connection is active
    (the line must be active)

    ForeignKeys are used since many Connections can be linked to a particular Line or Station, and
    should be deleted (models.CASCADE) if the Line or Station is deleted.
    """

    # line.connection.all() gives all connections associated with that line
    line = models.ForeignKey(Line, on_delete=models.CASCADE, related_name="connection")
    start_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="connection_start"
    )
    destination_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="connection_destination"
    )
    distance = models.FloatField(help_text="Distance in km", default=5)
    travel_time = models.PositiveIntegerField(help_text="time in minutes")
    cost = models.DecimalField(max_digits=15, decimal_places=2, default=10)

    # The Meta class in Django controls the behavior of the model without being involved in the
    # database. For instance, the unique_together will prevent entries if 2 connections have the 
    # same Line, start, and destination.
    class Meta:
        # Ensures connections can't have the same line, start, and destination
        unique_together = ("line", "start_station", "destination_station")

    def __str__(self):
        """Useful in the admin interface"""
        return f"{self.start_station} to {self.destination_station}, {self.line.name}"


class OTP(models.Model):
    """
    Defines the OTP model, needed for purchase confirmation.
    """
    user = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    code = models.CharField(max_length=OTP_LENGTH)
    creation_date = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return self.creation_date >= timezone.now() - timedelta(minutes=EXPIRYLIMIT)
