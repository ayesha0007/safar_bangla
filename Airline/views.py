# 




from django.http import JsonResponse
from django.shortcuts import render
from .models import Flights
from .forms import FlightForm
import json


JSON_FILE_PATH = r"C:\safar_bangla\data\flights.json"


# Function to load data from JSON file
def load_flights_from_json():
    with open(JSON_FILE_PATH, 'r', encoding='utf-8') as file:
        data = json.load(file)
        return data.get('Flights', [])  # Ensure we return the list of flights


def get_flights(request):
    # Load flight data from JSON file
    flights = load_flights_from_json()

    print(f"Flights retrieved: {flights}")  # Debugging

    return render(request, 'your_template.html', {'flights': flights})



def flight_booking(request, det_from, det_to, y=0):
    
    flights_data = load_flights_from_json()

    
    if not Flights.objects.exists():
        for flight in flights_data:

            Flights.objects.update_or_create(
                Flight_number=flight.get('Flight_number', "N/A"),
                defaults={
                    "Airline_name": flight.get('Airline_name', "Unknown"),
                    "From": flight.get('From', "N/A"),
                    "To": flight.get('To', "N/A"),
                    "Depart": flight.get('Depart', "N/A"),
                    "Capacity": flight.get('Capacity', 180),
                    "Price": flight.get('Price', 5000)
                }
            )

    
    F_form = FlightForm(request.POST or None)
    F_form.fields['Flight_Info_id'].queryset = Flights.objects.filter(From=det_from, To=det_to)

    if request.method == 'POST' and F_form.is_valid():
        customer = Profile.objects.get(user_id=request.user.id)
        cFlight = F_form.cleaned_data['Flight_Info_id']
        FTicket = int(F_form.cleaned_data['tickets'])
        Flight = Flights.objects.get(pk=cFlight.pk)

        if FTicket <= 0:
            return JsonResponse({"error": "Invalid number of tickets selected"}, status=400)

        
        F_form.instance.user = request.user
        F_form.save()

        return render(request, 'success.html', {"message": f"Flight {Flight} booked successfully!"})

    if y == 1:
        return F_form

    return render(request, 'index.html', {'Fform': F_form, 'det_from': det_from, 'det_to': det_to})
