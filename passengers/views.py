from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Passenger, Ticket, Station

def index(request):
    return render(request, "passengers/index.html")

def login(request):
    return render(request, "passengers/index.html")

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

    if request.method == "POST":
        start_id = request.POST.get("start_station")
        dest_id = request.POST.get("destination_station")

        if start_id == dest_id:
            return render(request, "passengers/purchase.html", {
                "stations": stations,
                "error": "Start and destination cannot be the same."
            })

        start_station = Station.objects.get(id=start_id)
        dest_station = Station.objects.get(id=dest_id)

        Ticket.objects.create(
            passenger=passenger,
            start_station=start_station,
            destination=dest_station,
            status="active",
        )

        return redirect("dashboard")

    context = {
        "stations": stations,
    }
    return render(request, "passengers/purchase.html", context)