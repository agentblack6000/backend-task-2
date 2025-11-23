from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .forms import TicketForm, TicketIncomingForm, TicketOutgoingForm
from passengers.pathfinder import shortest_path
from passengers.models import Ticket

def index(request):
    return render(request, "scanner/index.html")

def scan_tickets(request):
    return render(request, "scanner/scanner.html")

@login_required
def incoming(request):
    message = ""
    if request.method == "POST":
        form = TicketIncomingForm(request.POST)

        if form.is_valid():
            ticket_id = form.cleaned_data["ticket_id"]
            
            try:
                ticket = Ticket.objects.get(id=ticket_id, passenger=request.user.passenger)

                if ticket.status.lower() == "in use":
                    message = "Already scanned"
                elif ticket.status.lower() == "expired":
                    message = "Ticket expired"
                else:
                    ticket.status = "In Use"
                    ticket.save()
                    message = "Scanned and updated successfully"
            except Ticket.DoesNotExist:
                message = "Invalid ticket ID/ Ticket doesn't belong to this passenger"
    else:
        form = TicketIncomingForm()

    return render(request, "scanner/incoming.html", {"form": form, "message": message})

@login_required
def outgoing(request):
    message = ""
    if request.method == "POST":
        form = TicketOutgoingForm(request.POST)

        if form.is_valid():
            ticket_id = form.cleaned_data["ticket_id"]
            
            try:
                ticket = Ticket.objects.get(id=ticket_id, passenger=request.user.passenger)

                if ticket.status == "In Use":
                    ticket.status = "Expired"
                    ticket.save()
                    message = "Journey completed"
                elif ticket.status.lower() == "active":
                    message = "Invalid, go to the incoming platform"
                elif ticket.status == "Expired":
                    message = "Already scanned"
            except Ticket.DoesNotExist:
                message = "Invalid ticket ID/ Ticket doesn't belong to this passenger"
    else:
        form = TicketOutgoingForm()
    return render(request, "scanner/outgoing.html", {"form": form, "message": message})

@staff_member_required
def purchase_offline(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.status = "In Use"

            try:
                total_cost, total_distance, connections = shortest_path(ticket.start_station, ticket.destination)
                ticket.cost = total_cost
            except ValueError:
                # No route available
                return render(request, "scanner/purchase.html", {"form": form, "error": "No operational lines between these stations."})
            
            ticket.save()
            return redirect(request.path)
    else:
        form = TicketForm()

    return render(request, "scanner/purchase.html", {"form": form})