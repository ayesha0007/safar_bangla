
from django.urls import path
from . import views

from .views import all_link_view


urlpatterns = [
    path('',views.index,name="Home"),
    path('register/',views.Register,name='Register'),
    path('login/',views.Login,name='Login'),
    path('marks/', views.marks, name='marks'),
    path('logout/',views.Logout,name='Logout'),
    path('all-link/', all_link_view, name='all_link'),
    path('profile/<str:username>',views.profile,name='profile'),
    path('booking-list/<int:ID>',views.booking_list,name='booking_list'),
]