from django.core.mail import send_mail
from django.conf import settings
from .models import EXPIRYLIMIT
import random

OTP_LENGTH = 6


def generate_otp():
    otp = "".join([str(random.randint(0, 9)) for _ in range(OTP_LENGTH)])
    return otp


def send_verification_email(user_email, otp):
    subject = f"Your OTP is {otp}"
    message = f"Your OTP is {otp}, use it to verify the ticket purchase, expires in {EXPIRYLIMIT} minutes"

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])
