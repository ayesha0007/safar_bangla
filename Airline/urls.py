from django.urls import path
from . import views
# from .views import get_flights
from .views import get_biman_flights

urlpatterns = [
    # path('reserve/<str:det_from>TO<str:det_to>',views.flight_booking, name="flight"),
    # path('flights/', get_flights, name='get_flights'),
    path('biman-flights/', get_biman_flights, name="biman_flights")
]

