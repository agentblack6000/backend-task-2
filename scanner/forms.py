from django import forms
from passengers.models import Ticket


class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ["passenger", "start_station", "destination"]


class TicketIncomingForm(forms.Form):
    ticket_id = forms.IntegerField(label="Enter your ticket ID")


class TicketOutgoingForm(forms.Form):
    ticket_id = forms.IntegerField(label="Enter your ticket ID")
