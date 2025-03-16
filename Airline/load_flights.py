import json
from django.core.management.base import BaseCommand
from airline.models import Flights, Flight_Reserve

class Command(BaseCommand):
    help = 'Load flight data from a JSON file into the database'

    def handle(self, *args, **kwargs):
        # Path to your JSON file
        json_file_path = 'E:\safar_bangla\data\flights.json'

        try:
            # Open and load the JSON data
            with open(json_file_path, 'r') as file:
                data = json.load(file)

            # Insert flight data
            for flight_data in data['flights']:
                flight = Flights(
                    Airline_name=flight_data['Airline_name'],
                    From=flight_data['From'],
                    To=flight_data['To'],
                    Depart=flight_data['Depart'],
                    Price=flight_data['Price'],
                    Capacity=flight_data['Capacity']
                )
                flight.save()

            # Insert flight reservation data
            for reserve_data in data['flight_reservations']:
                flight_reservation = Flight_Reserve(
                    tickets=reserve_data['tickets'],
                    Flight_Info_id=Flights.objects.get(id=reserve_data['Flight_Info_id'])
                )
                flight_reservation.save()

            self.stdout.write(self.style.SUCCESS('Data loaded successfully'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Error occurred: {e}'))
