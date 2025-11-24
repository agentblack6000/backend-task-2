from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta
from passengers.pathfinder import shortest_path

EXPIRYLIMIT = 10


class Passenger(models.Model):
    bank_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Station(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Ticket(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in use", "In Use"),
        ("active", "Active"),
        ("expired", "Expired"),
    ]

    passenger = models.ForeignKey(
        Passenger, on_delete=models.CASCADE, related_name="tickets"
    )
    start_station = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="start_station"
    )
    destination = models.ForeignKey(
        Station, on_delete=models.CASCADE, related_name="destination_station"
    )
    cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")

    def calculate_cost(self, start_station, destination_station):
        try:
            cost, distance, stations_crossed = shortest_path(
                start_station, destination_station
            )
        except ValueError:
            return -1

        return cost

    def save(self, *args, **kwargs):
        self.cost = self.calculate_cost(self.start_station, self.destination)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.passenger.user.username}, {self.start_station.name} to {self.destination.name}"


class Line(models.Model):
    name = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        status = "active" if self.is_active else "disabled"
        return f"{self.name}, ({status})"


class Connection(models.Model):
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

    class Meta:
        unique_together = ("line", "start_station", "destination_station")

    def __str__(self):
        return f"{self.start_station} to {self.destination_station}, {self.line.name}"


class OTP(models.Model):
    user = models.ForeignKey(Passenger, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    creation_date = models.DateTimeField(auto_now_add=True)

    def is_valid(self):
        return self.creation_date >= timezone.now() - timedelta(minutes=EXPIRYLIMIT)
