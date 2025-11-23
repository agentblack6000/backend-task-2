from django import forms
from django.contrib.auth.models import User
from .models import Passenger

class PassengerSignupForm(forms.ModelForm):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Passenger
        fields = []

    def save(self):
        username = self.cleaned_data["username"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]

        # Create the Django user
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
        )

        # Create passenger linked to user
        passenger = Passenger.objects.create(
            user=user,
            bank_balance=0,
        )

        return passenger