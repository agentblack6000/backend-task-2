from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .forms import TicketForm
from passengers.pathfinder import shortest_path

def index(request):
    return render(request, "scanner/index.html")

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