from django.shortcuts import redirect, render
from django.http import HttpResponse, JsonResponse
from datetime import datetime
from .forms import ReserveForm
from .models import Reserve_Room, Room
from UserAccount.models import Profile
from UserAccount.decorators import superuser_required  # ✅ Import the custom decorator
import json
import os
from django.conf import settings

@superuser_required  # ✅ Now it will work correctly
def all_link_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'data', 'flights.json')  # ✅ Updated path

    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
    except FileNotFoundError:
        return JsonResponse({'error': 'flights.json not found'}, status=404)

    return JsonResponse(data, safe=False)

def booking(request, rtype):
    if request.method == 'POST':
        form = ReserveForm(request.POST)
        if form.is_valid():
            room = form.cleaned_data['Room_id']
            check_in = form.cleaned_data['Rcheck_in']
            check_out = form.cleaned_data['Rcheck_out']
            user = request.user

            available_rooms = Room.objects.filter(id=room.id)

            if available_rooms.exists():
                reserve = Reserve_Room(
                    user=user,
                    Room_id=room,
                    Rcheck_in=check_in,
                    Rcheck_out=check_out,
                )
                reserve.save()

                messages.success(request, f"Room {room} booked from {check_in} to {check_out}.")
                return redirect('booking', rtype)
            else:
                messages.error(request, "Room is unavailable.")
                return redirect('booking', rtype)
        else:
            messages.error(request, "Form is invalid.")
            return redirect('booking', rtype)
    else:
        form = ReserveForm()
    return render(request, 'hotel/booking.html', {'form': form, 'rtype': rtype})


def info_view(request):
    data = {
        "name": "Fahim Musubbir, Ayesha Shidika",
        "id": "2111476, 2221891",
        "personal_notion_page": "//",  # Link or placeholder
        "personal_group_page_notion": "//",  # Link or placeholder
        "github_id": "mridhafahim, ayesha0007",
        "project_github_link": "https://github.com/ayesha0007/safar_bangla.git"
    }
    
    return JsonResponse(data)  # Return data as JSON response
