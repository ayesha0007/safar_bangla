from django.db import models
from django.contrib.auth.models import User
# Create your models here.


# class Flights(models.Model):
    # Companies = (
    #     ('EGA', 'Egypt Air'),
    #     ('NIA', 'Nile Air'),
    #     ('ARA', 'Arabic Air'),
    # )
    # Locations = (
    #     ('CAI', 'Cairo Airport'),
    #     ('HGR', ' Hurghada Airport'),
    #     ('HBE', 'Borg El Arab Airport'),
    #     ('SSH', 'Sharm El Sheikh Airport'),
    # )

    # Airline_name = models.CharField(
    #     max_length=15, choices=Companies, default="Egypt Air")
    # From = models.CharField(
    #     max_length=30, choices=Locations, default="Cairo Airport")
    # To = models.CharField(max_length=30, choices=Locations,
    #                       default="Hurghada Airport")
    # Depart = models.DateTimeField()
    # Capacity = models.IntegerField(default=30)
    # Price = models.FloatField()


    
    # def __str__(self):
    #     return f"""{self.tickets} tickets for flight {self.Flight_Info_id.get_Airline_name_display()} 
    #     from {self.Flight_Info_id.From} to {self.Flight_Info_id.To} at {self.Flight_Info_id.Depart}"""



# class Flights(models.Model):
#     Airline_name = models.CharField(max_length=50)  
#     # flight_number = models.CharField(max_length=10, unique=True)  
#     # From = models.CharField(max_length=50)
#     # To = models.CharField(max_length=50)
#     # Depart = models.DateTimeField()
#     # Arrival = models.DateTimeField(null=True, blank=True)  
#     # Capacity = models.IntegerField(default=30)
#     # Available_seats = models.IntegerField(default=30)  
#     # Price = models.FloatField()
#     id = 
#     Airline_name = models.CharField(max_length=50)
#     From = models.CharField(max_length=50)
#     To = models.CharField(max_length=50)
#     Depart =models.DateTimeField()
#     Price = models.FloatField()
#     Capacity = models.IntegerField(default=30)


#     def __str__(self):
#         return f"{self.Airline_name} flight from {self.From} to {self.To}, departs at {self.Depart}, Price: ${self.Price}"


# class Flight_Reserve(models.Model):
#     # user = models.ForeignKey(User, on_delete=models.CASCADE)
#     # Flight_Info_id = models.ForeignKey(Flights, on_delete=models.CASCADE)  # ✅ FIXED: Changed 'Flight_Info_id' → 'Flights'
#     # tickets = models.IntegerField()
#     id = 
#     tickets = models.IntegerField()
#     Flight_Info_id_id = models.ForeignKey(Flights, on_delete=models.CASCADE)  # ✅ FIXED: Changed 'Flight_Info_id' → 'Flights'
#     user_id = 
# from django.db import models

class Flights(models.Model):
    # Fields for the flight model
    Airline_name = models.CharField(max_length=50)
    From = models.CharField(max_length=50)
    To = models.CharField(max_length=50)
    Depart = models.DateTimeField()
    Price = models.FloatField()
    Capacity = models.IntegerField(default=30)
    # Available_seats = models.IntegerField(default=30)  # You may want to track available seats
    
    def __str__(self):
        return f"{self.Airline_name} flight from {self.From} to {self.To}, departs at {self.Depart}, Price: ${self.Price}"


class Flight_Reserve(models.Model):
    # Fields for the flight reservation model
    tickets = models.IntegerField()
    Flight_Info_id = models.ForeignKey(Flights, on_delete=models.CASCADE)
    user_id = models.IntegerField()  # Assuming you want to store user ID as a simple IntegerField

    def __str__(self):
        return f"Reservation for {self.Flight_Info_id.Airline_name} from {self.Flight_Info_id.From} to {self.Flight_Info_id.To}, Tickets: {self.tickets}"

   

    def __str__(self):
        return f"{self.tickets} tickets for {self.Flight_Info_id.Airline_name} flight from {self.Flight_Info_id.From} to {self.Flight_Info_id.To} at {self.Flight_Info_id.Depart}"
