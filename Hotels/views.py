# 

from django.shortcuts import redirect, render
from django.http import HttpResponse
from datetime import datetime
from .forms import ReserveForm
from .models import Reserve_Room, Room
from UserAccount.models import Profile
import json
import os
from django.http import JsonResponse
from django.core.exceptions import PermissionDenied
from django.conf import settings


@superuser_required
def all_link_view(request):
    # Path to the flights.json file
    file_path = os.path.join(settings.BASE_DIR, 'your_app_name', 'flights.json')  # Change 'your_app_name'
    
    with open(file_path, 'r') as file:
        data = json.load(file)
    return JsonResponse(data, safe=False)

def info_view(request):
    data = {
        "name": "Fahim Musubbir , Ayesha Shidika",
        "id": "2111476 , 2221891",
        "personal_notion_page": "//",
        "personal_group_page_notion": "//",
        "github_id": "mridhafahim , ayesha0007",
        "project_github_link": "omyouhttps://github.com/ayesha0007/safar_bangla.git"
    }
    return JsonResponse(data)

# Create your views here.
def booking(request, rtype, x=0):
    form = ReserveForm(request.POST or None)
    form.fields['Room_id'].queryset = Room.objects.filter(Rcategory=rtype)  # Filter rooms based on rtype

    if request.method == 'POST' and form.is_valid():
        # Cleaned data from the form
        form_checkIn = form.cleaned_data['Rcheck_in']
        form_checkOut = form.cleaned_data['Rcheck_out']
        Croom = form.cleaned_data['Room_id']

        customer = Profile.objects.get(user_id=request.user.id)
        room_details = Room.objects.get(pk=Croom.pk)

        # Check if the check-in time is before the check-out time
        if form_checkIn < form_checkOut:
            # Check if the room is available
            existing_reservations = Reserve_Room.objects.filter(Room_id=Croom)

            # Check if any of the existing bookings overlap with the new booking
            for reservation in existing_reservations:
                if not (reservation.Rcheck_out <= form_checkIn or reservation.Rcheck_in >= form_checkOut):
                    return HttpResponse("The room is not available for the selected dates.")

            # No overlapping bookings, proceed with the reservation
            form.instance.user = request.user
            form.save()

            # Adjust the amount to be paid based on VIP status
            if customer.vip:
                customer.amount_to_pay += room_details.price * 0.9  # 10% discount for VIPs
            else:
                customer.amount_to_pay += room_details.price
            customer.save()

            return HttpResponse("You are successfully booked.")

        else:
            return HttpResponse("Please enter a valid time period. Check-out must be after check-in.")

    # If `x == 1`, return the form, otherwise render the page with the form
    if x == 1:
        return form

    return render(request, 'index.html', {'form': form, 'rtype': rtype})


