from django import forms
from .models import Flight_Reserve
# from .models import Flight_Info_id
from Airline.models import Flights


class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight_Reserve
        fields = ['Flight_Info_id', 'tickets']
