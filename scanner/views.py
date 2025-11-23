from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect
from .forms import TicketForm

def index(request):
    return render(request, "scanner/index.html")

@staff_member_required
def purchase_offline(request):
    if request.method == "POST":
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.status = "In Use"
            ticket.save()
        
            return redirect(request.path)
    else:
        form = TicketForm()

    return render(request, "scanner/purchase.html", {"form": form})