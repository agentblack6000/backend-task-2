"""
Implements the forms used:

PassengerSignupForm: For registering new users
AddMoneyForm: To add balance to the passenger accounts
OTPForm: OTP verification on the confirmation page

The Decimal class is used here to deal with the bank balance since its related to finances, given the
issues that come with representing decimal numbers in binary
The Django forms model is used to implement the forms
The User model is key for builtin Django authenticaiton
The Passenger model is tied to the PassengerSignupForm
"""
from decimal import Decimal
from django import forms
from django.contrib.auth.models import User
from .models import Passenger
from .otp_generation import OTP_LENGTH

# The Django forms module provides classes and other tools to create HTML forms, validating user input,
# handling security issues like CSRF and injection
# forms.Form is the most basic form class, used when the form doesn't have any link with the database
# and provides full manual control over the data collected
# forms.ModelForm connects the form to a Django model, and automatically generates and validates the fields
# needed in the model.
class PassengerSignupForm(forms.ModelForm):
    """
    Implements the form for registering new users
    """

    # Here although we're manually defining the fields, we want the form to be tied to the Passenger
    # model since a Passenger has a User (for Django authentication) and their bank balance associated
    # with them.
    username = forms.CharField(max_length=150)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    # The Meta class tells Django what model the form is associated with, what fields
    # to include/exclude, and other things like widgets or custom help text can be specified here
    class Meta:
        model = Passenger
        # This telss Django not to auto-generate any fields based on the model
        fields = []

    def save(self):
        """
        Part of Django's ORM, provides INSERT or UPDATE operations. In this case, since this is a
        signup form, INSERT operations are being performed to add a new Passenger to the database
        Every Django model has a save method, and since the PassengerSignupForm is based on the
        Passenger model, the save() method updates or creates a new instance of the Passenger in the
        database
        """
        username = self.cleaned_data["username"]
        first_name = self.cleaned_data["first_name"]
        last_name = self.cleaned_data["last_name"]
        email = self.cleaned_data["email"]
        password = self.cleaned_data["password"]

        # Create the Django user
        # The create_user() method is part of Django's UserManager and is needed over
        # just create() here since it performs password hashing and automatically sets some
        # defaults like is_staff = False
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name,
        )

        # Create passenger linked to user
        # All Django models have a create() method, adds a new row to the database with the values
        # passed.
        passenger = Passenger.objects.create(
            user=user,
            bank_balance=0,  # default bank balance is set to 0
        )

        return passenger


class AddMoneyForm(forms.Form):
    """
    Enables Passengers to add money to their accounts to purchase tickets. A normal forms.Form is
    used here over a ModelForm since we only have one field to validate, we don't need Django's
    auto-generation or a new database to associate this with.

    This form collects a decimal number from the user and performs the necessary validation for it
    """

    amount = forms.DecimalField(
        min_value=Decimal("0.01"),
        max_digits=6,
        decimal_places=2,
        label="Amount",
        # The widget helps control the form's HTML, in this case it helps provide
        # better styling and gives some placeholder text over using Django's
        # default NumberInput()
        widget=forms.NumberInput(
            # This adds the form-control class for Bootstrap styling, and
            # the placeholder is the grayed out text in the input
            attrs={"class": "form-control", "placeholder": "0.00"}
        ),
    )


class OTPForm(forms.Form):
    """
    Handles OTP validation. A normal forms.Form is used here because we don't need to associate this
    with any model/database.

    A CharField is used over an IntegerField to preserve the leading zeroes in the OTP (if any)
    Also since no numeric operations are being performed on the OTP a CharField is the best for this
    scenario.
    """

    otp = forms.CharField(
        max_length=OTP_LENGTH,
        min_length=OTP_LENGTH,
        label="Enter OTP",
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": f"Enter {OTP_LENGTH} digit OTP",
                "autocomplete": "off",
            }
        ),
    )
