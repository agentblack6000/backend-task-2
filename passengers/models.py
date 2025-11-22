from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Passenger(models.Model):
    bank_balance = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Station(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    STATUS_CHOICES = [
        ("in use", "In Use"),
        ("active", "Active"),
        ("expired", "Expired"),
    ]


    passenger = models.ForeignKey(Passenger, on_delete=models.CASCADE, related_name="tickets")
    start_station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="start_station")
    destination = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="destination_station")
    cost = models.DecimalField(max_digits=10, decimal_places=2, editable=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)

    def save(self, *args, **kwargs):
        self.cost = 100
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.passenger.user.username}, {self.start_station.name} to {self.destination.name}"
