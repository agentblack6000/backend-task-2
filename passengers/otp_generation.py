"""
Sets up OTP verification using the Django core module
"""
from django.core.mail import send_mail
from django.conf import settings
from .models import EXPIRYLIMIT, OTP_LENGTH
import random


def generate_otp():
    """Random string of 6 digits, an integer range can't be used since the leading zeros would lose meaning"""
    otp = "".join([str(random.randint(0, 9)) for _ in range(OTP_LENGTH)])
    return otp


def send_verification_email(user_email, otp):
    """Sends the OTP verification email"""
    subject = f"Your OTP is {otp}"
    message = f"Your OTP is {otp}, use it to verify the ticket purchase, expires in {EXPIRYLIMIT} minutes"

    send_mail(subject, message, settings.EMAIL_HOST_USER, [user_email])
