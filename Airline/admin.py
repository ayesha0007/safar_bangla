# from django.contrib import admin
# from .models import Flights, Flight_Reserve
# # Register your models here.
# admin.site.register(Flights)
# admin.site.register(Flight_Reserve)


from django.contrib import admin
from .models import Flights, Flight_Reserve

@admin.register(Flights)
class FlightsAdmin(admin.ModelAdmin):
    list_display = ('Airline_name', 'From', 'To', 'Depart', 'Capacity', 'Price')  # Display these fields in admin
    list_filter = ('Airline_name', 'From', 'To', 'Depart')  # Filter sidebar
    search_fields = ('Airline_name', 'From', 'To')  # Search flights
    ordering = ('Depart',)  # Order by departure time
    list_editable = ('Capacity', 'Price')  # Allow direct editing
    readonly_fields = ('Depart',)  # Prevent accidental changes

@admin.register(Flight_Reserve)
class FlightReserveAdmin(admin.ModelAdmin):
    list_display = ('user', 'Flight_Info', 'tickets')  # Show these in admin panel
    list_filter = ('user', 'Flight_Info')  # Filter sidebar
    search_fields = ('user__username', 'Flight_Info__Airline_name')  # Search by username & flight
    readonly_fields = ('Flight_Info', 'user')  # Prevent modifying these

