from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Passenger, Ticket, Station
from .signup_form import PassengerSignupForm

def index(request):
    return render(request, "passengers/index.html")

def login(request):
    return render(request, "passengers/index.html")

def signup(request):
    if request.method == "POST":
        form = PassengerSignupForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("passenger-login")
    else:
        form = PassengerSignupForm()
    
    return render(request, "passengers/signup.html", {"form": form})

@login_required
def dashboard(request):
    passenger = request.user.passenger
    tickets = passenger.tickets.all()

    context = {
        "passenger": passenger,
        "tickets": tickets,
    }

    return render(request, "passengers/dashboard.html", context)

@login_required
def purchase(request):
    passenger = request.user.passenger
    stations = Station.objects.all()
    context = {
        "stations": stations,
    }

    if request.method == "POST":
        start_station_id = request.POST.get("start_station")
        dest_station_id = request.POST.get("destination_station")

        if start_station_id == dest_station_id:
            return render(request, "passengers/purchase.html", {
                "stations": stations,
                "error": "Start and destination cannot be the same."
            })

        start_station = Station.objects.get(id=start_station_id)
        dest_station = Station.objects.get(id=dest_station_id)

        temp_ticket = Ticket(passenger=passenger, start_station=start_station, destination=dest_station)
        cost = temp_ticket.calculate_cost(start_station, dest_station)

        if passenger.bank_balance < cost:
            context["error"] = "Insufficent balance"
            return render(request, "passengers/purchase.html", context)
        
        passenger.bank_balance -= cost
        passenger.save()

        temp_ticket.status = "active"
        temp_ticket.save()

        messages.success(request, "Purchase successful")
        return redirect("dashboard")


    return render(request, "passengers/purchase.html", context)