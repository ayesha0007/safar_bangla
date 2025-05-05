fixfrom django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import ProfileForm
from .models import Profile
from django.contrib.auth import authenticate, login, logout
from Hotels.views import booking
from Airline.views import flight_booking
from Hotels.models import Reserve_Room
from Airline.models import Flight_Reserve, Flights
from django.http import JsonResponse, HttpResponseForbidden
from django.conf import settings
from .decorators import superuser_required
import os
import json

# Create your views here.

def marks(request):
    return render(request, 'marks.html')


@superuser_required
def all_link_view(request):
    file_path = os.path.join(settings.BASE_DIR, 'your_app_name', 'flights.json')  # Replace 'your_app_name'!
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
        "project_github_link": "https://github.com/ayesha0007/safar_bangla.git"
    }
    return JsonResponse(data)


def index(request):
    rtype = request.GET.get('rtype')
    det_to = request.GET.get('det_to')
    det_from = request.GET.get('det_from')
    prof = "False"
    if request.user.id is not None:
        prof = Profile.objects.get(user_id=request.user)

    if 'Hotels' in request.GET and rtype:
        return redirect('booking', rtype)

    if 'Flights' in request.GET and det_to != 'None' and det_from != 'None':
        return redirect('flight', det_from, det_to)

    return render(request, 'index.html', {'rtype': rtype, 'det_to': det_to, 'det_from': det_from, 'profile': prof})


def Login(request):
    if request.method == 'POST':
        usern = request.POST['username']
        pass1 = request.POST['Password1']
        user = authenticate(request, username=usern, password=pass1)
        if user is not None:
            login(request, user)
            return redirect('Home')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('Login')
    return render(request, 'login.html')


def Register(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        usern = request.POST['username']
        fname = request.POST['FirstName']
        lname = request.POST['LastName']
        Email = request.POST['EMAIL']
        pass1 = request.POST['Password1']
        pass2 = request.POST['Password2']
        if pass1 == pass2:
            if User.objects.filter(email=Email).exists():
                messages.info(request, 'Email exists')
                return redirect('Register')
            elif User.objects.filter(username=usern).exists():
                messages.info(request, 'Username exists')
                return redirect('Register')
            else:
                Nuser = User.objects.create_user(
                    username=usern, first_name=fname, last_name=lname, email=Email,
                    password=pass1
                )
                if form.is_valid():
                    event = form.save(commit=False)
                    event.user = Nuser
                    event.save()
                return redirect('Login')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('Register')
    else:
        form = ProfileForm()
    return render(request, 'Register.html', {'form': form})


def Logout(request):
    if request.method == 'POST':
        logout(request)
    return redirect('Login')


def profile(request, username):
    user = User.objects.get(username=username)
    prof = Profile.objects.get(user_id=request.user.id)
    change = 0
    if request.method == 'POST':
        if "UPDATE" in request.POST:
            change = 1
        elif "SAVE" in request.POST:
            user.first_name = request.POST['firstName']
            user.last_name = request.POST['lastName']
            user.email = request.POST['EMAIL']
            user.save()
            return redirect('profile', username)
    return render(request, 'profile.html', {'prof': prof, 'change': change})


def booking_list(request, ID):
    flights = Flight_Reserve.objects.filter(user_id=ID)
    rooms = Reserve_Room.objects.filter(user_id=ID)
    customer = Profile.objects.get(user_id=ID)

    if request.method == 'POST':
        if 'Droom' in request.POST:
            DRoom = Reserve_Room.objects.get(id=request.POST['Droom'])
            discount = 0.1 if customer.vip else 0
            customer.amount_to_pay -= DRoom.Room.price * (1 - discount)
            customer.save()
            DRoom.delete()

        if 'Dflight' in request.POST:
            DFlight = Flight_Reserve.objects.get(id=request.POST['Dflight'])
            flight_price = DFlight.Flight_Info_id.Price
            tickets = DFlight.tickets
            discount = 0.1 if customer.vip else 0
            customer.amount_to_pay -= (flight_price * tickets) * (1 - discount)
            customer.save()

            flight = Flights.objects.get(id=DFlight.Flight_Info_id.id)
            flight.Capacity += tickets
            flight.save()

            DFlight.delete()

    return render(request, 'Cart.html', {'rooms': rooms, 'flights': flights})
