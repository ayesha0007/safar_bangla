# from django.contrib import admin
# from .models import Flights, Flight_Reserve
# # Register your models here.
# admin.site.register(Flights)
# admin.site.register(Flight_Reserve)


from django.contrib import admin
from .models import Flight_Reserve, Flights 

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
    list_display = ('user_id', 'Flight_Info_id', 'tickets')  # Show these in admin panel
    list_filter = ('user_id', 'Flight_Info_id', 'tickets')  # Filter sidebar 
    search_fields = ('user__username', 'Flight_Info_id__Airline_name')  # Search by username & flight
    readonly_fields = ('Flight_Info_id', 'user_id', 'tickets')  # Prevent modifying these
    def user(self, obj):
        # If you have a ForeignKey to a user, access it like this
        return obj.user_id
    user.short_description = 'User'  # Optional: To give a custom name in admin display

# admin.site.register(Flight_Reserve, FlightReserveAdmin)

