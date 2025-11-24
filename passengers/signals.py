from allauth.account.signals import user_signed_up
from django.dispatch import receiver
from .models import Passenger


@receiver(user_signed_up)
def create_passenger_on_signup(request, user, **kwargs):
    Passenger.objects.create(user=user)
