"""
Implements the views used in the app.

The authentication decorator (login_required) is used to protect pages meant to have a user associated
with them (ex. dashboard)
IntegrityError is needed to catch users trying to reuse the same username/email
Decimal is used when updating user bank balance
"""
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import IntegrityError
from django.shortcuts import render, redirect
from .models import Ticket, Station, OTP
from .forms import PassengerSignupForm, OTPForm, AddMoneyForm
from .otp_generation import generate_otp, send_verification_email

from decimal import Decimal


def index(request):
    """Renders the login page"""
    return render(request, "passengers/index.html")


def login(request):
    """Renders the login page"""
    return render(request, "passengers/index.html")


def signup(request):
    """
    Implements user sign up
    """
    if request.method == "POST":
        # Associates the Django form with the request data
        form = PassengerSignupForm(request.POST)

        # Performs validation, catches IntegrityError if the same username/email is 
        # used twice
        if form.is_valid():
            try:
                form.save()
                return redirect("passenger-login")
            except IntegrityError as e:
                messages.error(request, "Username/email already exists")
        else:
            messages.error(request, "Invalid form")
    else:
        form = PassengerSignupForm()

    return render(request, "passengers/signup.html", {"form": form})


@login_required
def dashboard(request):
    """
    Renders the user dashboard, displaying all their tickets
    """
    passenger = request.user.passenger
    tickets = passenger.tickets.all()

    context = {
        "passenger": passenger,
        "tickets": tickets,
    }

    return render(request, "passengers/dashboard.html", context)


@login_required
def purchase(request):
    """
    Handles ticket purchasing
    """
    passenger = request.user.passenger
    stations = Station.objects.all()
    context = {
        "stations": stations,
    }

    if request.method == "POST":
        start_station_id = request.POST.get("start_station")
        dest_station_id = request.POST.get("destination_station")

        if start_station_id == dest_station_id:
            return render(
                request,
                "passengers/purchase.html",
                {
                    "stations": stations,
                    "error": "Start and destination cannot be the same.",
                },
            )

        start_station = Station.objects.get(id=start_station_id)
        dest_station = Station.objects.get(id=dest_station_id)

        temp_ticket = Ticket(
            passenger=passenger, start_station=start_station, destination=dest_station
        )
        cost = temp_ticket.calculate_cost(start_station, dest_station)

        if cost < 0:
            context["error"] = "No metro lines operational that cover that route"
            return render(request, "passengers/purchase.html", context)

        if passenger.bank_balance < cost:
            context["error"] = "Insufficent balance"
            return render(request, "passengers/purchase.html", context)

        temp_ticket.status = "pending"
        temp_ticket.save()

        return redirect("confirmation", ticket_id=temp_ticket.id)

    return render(request, "passengers/purchase.html", context)


@login_required
def add_money(request):
    """
    Enables users to add balance to their accounts
    """
    passenger = request.user.passenger

    if request.method == "POST":
        # Associates the Django form with the request data
        form = AddMoneyForm(request.POST)

        # Checks if form is valid
        if form.is_valid():
            amount = Decimal(form.cleaned_data["amount"])

            # Updates user bank balance
            passenger.bank_balance += amount
            passenger.save()

            return redirect("dashboard")
    else:
        form = AddMoneyForm()

    return render(request, "passengers/money.html", {"form": form})


@login_required
def confirmation(request, ticket_id):
    """
    Confirms purchase on OTP verificatoin, deducts balance, marks ticket as active
    """
    passenger = request.user.passenger
    ticket = Ticket.objects.get(id=ticket_id)

    form = OTPForm()

    if request.method == "GET":
        # Generates and creates an OTP
        user_otp = generate_otp()
        OTP.objects.create(user=passenger, code=user_otp)

        # Sends the verification email
        send_verification_email(request.user.email, user_otp)
    elif request.method == "POST":
        form = OTPForm(request.POST)

        # Checks if form is valid
        if form.is_valid():
            user_otp = form.cleaned_data["otp"]
            otp_database_log = OTP.objects.filter(user=passenger, code=user_otp).last()

            # Check if entered OTP exists and is valid
            if otp_database_log and otp_database_log.is_valid():
                # Updates ticket status and deducts cost
                ticket.status = "active"
                passenger.bank_balance -= ticket.cost

                passenger.save()
                ticket.save()

                return redirect("dashboard")
            else:
                messages.error(request, "Invalid or expired OTP")

    return render(
        request, "passengers/confirmation.html", {"ticket": ticket, "form": form}
    )
