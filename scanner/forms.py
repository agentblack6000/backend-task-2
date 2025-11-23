from django import forms
from passengers.models import Ticket, Station, Passenger

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['passenger', 'start_station', 'destination']
        # cost is calculated automatically if you keep it in the Ticket model
