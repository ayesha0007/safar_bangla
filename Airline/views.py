# # from django.http import HttpResponse
# # from django.shortcuts import render
# # from .forms import FlightForm
# # from .models import Flights
# # from UserAccount.models import Profile
# # # Create your views here.


# # def flight_booking(request, det_from, det_to, y=0):

# #     F_form = FlightForm(request.POST)
# #     F_form.fields['Flight_Info_id'].queryset = Flights.objects.filter(
# #         From=det_from, To=det_to).exclude(Capacity=0)

# #     if request.method == 'POST':

# #         if F_form.is_valid():

# #             customer = Profile.objects.get(user_id=request.user.id)
# #             cFlight = F_form['Flight_Info_id'].value()
# #             FTicket = int(F_form['tickets'].value())
# #             Flight = Flights.objects.get(pk=cFlight)

# #             if Flight.Capacity <= 0:
# #                 return HttpResponse(f'This flight is full')

# #             elif FTicket > Flight.Capacity:
# #                 return HttpResponse(f"U selected {FTicket} tickets and this flight has only {Flight.Capacity} tickets remaining")
# #             elif FTicket <= 0:
# #                 return HttpResponse(f"U selected {FTicket} tickets please enter a vaild number")
# #             else:
# #                 F_form.instance.user = request.user
# #                 F_form.save()
# #                 if customer.vip:
# #                   customer.amount_to_pay += (Flight.Price * FTicket) * (1- 0.1)
# #                   customer.save()
# #                 else:
# #                    customer.amount_to_pay += Flight.Price * FTicket
# #                    customer.save()
# #                 Flight.Capacity -= FTicket
# #                 Flight.save()
# #                 return HttpResponse(f'Ur Flight of {Flight} is booked ')

# #     if(y == 1):
# #         return F_form
# #     return render(request, 'index.html', {'Fform': F_form, 'det_from': det_from, 'det_to': det_to})


# from django.http import HttpResponse, JsonResponse
# from django.shortcuts import render
# from .forms import FlightForm
# from .models import Flights
# from UserAccount.models import Profile
# import requests

# # Bangladesh Airlines API URL (Example)
# API_URL = "https://api.aviationstack.com/v1/flights?access_key=047783721ec985f2344f9b12182a9a67"

# def get_flights(request):
#     """
#     Returns all flights stored in the database.
#     """
#     flights = Flights.objects.all().values()
#     return JsonResponse(list(flights), safe=False)


# def fetch_flights_from_api(det_from, det_to):
#     """
#     Fetch flights dynamically from Bangladesh Airlines API.
#     """
#     params = {
#         "dep_iata": det_from,
#         "arr_iata": det_to,
#         "limit": 5  # Fetch up to 5 flights only
#     }
#     response = requests.get(API_URL, params=params)

#     if response.status_code == 200:
#         flight_data = response.json().get("data", [])  # API response structure check
#         return flight_data
#     return []  # Return empty list if API fails


# def flight_booking(request, det_from, det_to, y=0):
#     """
#     Handles flight booking process.
#     """
#     # Fetch flights dynamically from API
#     api_flights = fetch_flights_from_api(det_from, det_to)

#     # Store API flights into the database if not already stored
#     for flight in api_flights:
#         Flights.objects.update_or_create(
#             Flight_number=flight.get('flight.iata', "N/A"),
#             defaults={
#                 "Airline_name": flight.get('airline.name', "Unknown"),
#                 "From": flight.get('departure.iata', det_from),
#                 "To": flight.get('arrival.iata', det_to),
#                 "Depart": flight.get('departure.scheduled', "N/A"),
#                 "Arrival": flight.get('arrival.scheduled', "N/A"),
#                 "Capacity": flight.get('aircraft.capacity', 180),  # Default to 180 if not provided
#                 # "Available_seats": flight.get('aircraft.available_seats', 180),  # Default to full capacity
#                 "Price": flight.get('price', 5000)  # Default price if not provided
#             }
#         )

#     # Create Flight Booking Form
#     F_form = FlightForm(request.POST or None)
#     F_form.fields['Flight_Info_id'].queryset = Flights.objects.filter(
#         From=det_from, To=det_to) #.exclude(Available_seats=0)

#     if request.method == 'POST' and F_form.is_valid():
#         customer = Profile.objects.get(user_id=request.user.id)
#         cFlight = F_form.cleaned_data['Flight_Info_id']
#         FTicket = int(F_form.cleaned_data['tickets'])
#         Flight = Flights.objects.get(pk=cFlight.pk)

#         # API Sync - Check latest seat availability
#         latest_flights = fetch_flights_from_api(det_from, det_to)
#         for latest in latest_flights:
#             if latest.get('flight.iata') == Flight.Flight_number:
#                 # Flight.Available_seats = latest.get('aircraft.available_seats', Flight.Available_seats)
#                 Flight.save()

#         # # Validation Checks
#         # # if Flight.Available_seats <= 0:
#         # #     return HttpResponse(f'This flight is full')

#         # # elif FTicket > Flight.Available_seats:
#         # #     return HttpResponse(f"Selected {FTicket} tickets but only {Flight.Available_seats} available")

#         # elif FTicket <= 0:
#         #     return HttpResponse(f"Invalid number of tickets selected")

#         # else:
#         #     # Save Booking
#         #     F_form.instance.user = request.user
#         #     F_form.save()

#         #     # Update Customer Payment
#         #     discount = 0.1 if customer.vip else 0
#         #     customer.amount_to_pay += (Flight.Price * FTicket) * (1 - discount)
#         #     customer.save()

#         #     # Update Flight Seat Availability
#         #     Flight.Available_seats -= FTicket
#         #     Flight.save()

#         #     return render(request, 'success.html', {"message": f"Flight {Flight} booked successfully!"})

#     if y == 1:
#         return F_form

#     return render(request, 'index.html', {'Fform': F_form, 'det_from': det_from, 'det_to': det_to})

from django.http import JsonResponse
from django.shortcuts import render
from .models import Flights
import json

# Path to the JSON file (ensure the path is correct)
JSON_FILE_PATH = r"E:\safar_bangla\data\flights.json"


# Function to load data from JSON file
def load_flights_from_json():
    with open(JSON_FILE_PATH, 'r') as file:
        return json.load(file)

def get_flights(request):
    # Get the 'det_from' and 'det_to' from the URL parameters (GET request)
    det_from = request.GET.get('det_from', None)
    det_to = request.GET.get('det_to', None)

    # Debugging: Log the parameters received
    print(f"det_from: {det_from}, det_to: {det_to}")

    # If the user selected both departure and destination, filter the flights by those

    if det_from and det_to:
        flights = Flights.objects.filter(From=det_from, To=det_to)
    else:
        flights = Flights.objects.all()  # Get all flights if no specific destination is chosen

    # Debugging: Log the flights being passed to the template
    print(f"Flights retrieved: {list(flights)}")

    # Pass the flight data and destination details to the template

    return render(request, 'your_template.html', {'flights': flights, 'det_from': det_from, 'det_to': det_to})

def flight_booking(request, det_from, det_to, y=0):
    """
    Handles flight booking process. This can now fetch data from JSON.
    """
    # Instead of fetching from the API, we'll just use the local JSON data
    flights_data = load_flights_from_json()

    # Store the flights into the database if not already stored (this is based on your existing logic)
    for flight in flights_data:
        Flights.objects.update_or_create(
            Flight_number=flight.get('flight_number', "N/A"),
            defaults={
                "Airline_name": flight.get('Airline_name', "Unknown"),
                "From": flight.get('From', det_from),
                "To": flight.get('To', det_to),
                "Depart": flight.get('Depart', "N/A"),
                "Arrival": flight.get('Arrival', "N/A"),
                "Capacity": flight.get('Capacity', 180),
                "Price": flight.get('Price', 5000)
            }
        )

    # Your existing flight booking form logic goes here, no change needed for the form part.
    # (The rest of your flight_booking code remains the same)
    # Create Flight Booking Form
    F_form = FlightForm(request.POST or None)
    F_form.fields['Flight_Info_id'].queryset = Flights.objects.filter(
        From=det_from, To=det_to) #.exclude(Available_seats=0)

    if request.method == 'POST' and F_form.is_valid():
        customer = Profile.objects.get(user_id=request.user.id)
        cFlight = F_form.cleaned_data['Flight_Info_id']
        FTicket = int(F_form.cleaned_data['tickets'])
        Flight = Flights.objects.get(pk=cFlight.pk)

        # API Sync - Check latest seat availability
        latest_flights = fetch_flights_from_api(det_from, det_to)
        for latest in latest_flights:
            if latest.get('flight.iata') == Flight.Flight_number:
                # Flight.Available_seats = latest.get('aircraft.available_seats', Flight.Available_seats)
                Flight.save()
    if y == 1:
        return F_form

    return render(request, 'index.html', {'Fform': F_form, 'det_from': det_from, 'det_to': det_to})
