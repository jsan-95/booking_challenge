from django.shortcuts import render

from booking.models import Booking


def home(request):
    bookings = Booking.objects.all()
    return render(request, 'home.html', {'bookings': bookings})
