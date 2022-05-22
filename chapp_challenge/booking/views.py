from datetime import datetime
from django.shortcuts import get_object_or_404, redirect, render
from booking.forms import BookingDatesForm, BookingForm, BookingSearchRoomForm
from booking.models import Booking, Room


def booking_detail(request, booking_id):
    booking = get_object_or_404(Booking, pk=booking_id)
    return render(request, 'booking/detail.html', {'booking': booking})


def search_room(request):
    if request.method == 'POST':
        bookingSearchRoomForm = BookingSearchRoomForm(request.POST)
        if bookingSearchRoomForm.is_valid():
            return redirect('new_booking/' +
                            str(bookingSearchRoomForm.cleaned_data[
                                    'room'].id) + '/' +
                            bookingSearchRoomForm.data.get('check_in') + '/' +
                            bookingSearchRoomForm.data.get('check_out') + '/' +
                            str(bookingSearchRoomForm.cleaned_data[
                                    'guests']) + '/' +
                            str(bookingSearchRoomForm.cleaned_data[
                                    'total_price']))

        bookingDatesForm = BookingDatesForm(request.POST)
        if bookingDatesForm.is_valid():
            check_in = datetime.strptime(
                    bookingDatesForm['check_in'].data, '%Y-%m-%d')
            check_out = datetime.strptime(
                    bookingDatesForm['check_out'].data, '%Y-%m-%d')
            guests = bookingDatesForm['guests'].data

            bookings_check_in = Booking.objects.filter(
                    check_in__gte=check_in, check_out__lt=check_in)
            bookings_check_out = Booking.objects.filter(
                    check_in__lt=check_out, check_out__gte=check_out)
            bookings = bookings_check_in | bookings_check_out

            room_occupation = {room.id: room.max_availability for room in
                               Room.objects.all()}
            for booking in bookings:
                room_occupation[booking.room.id] -= 1

            room_ids_with_availability = [key for key, value in
                                          room_occupation.items() if value > 0]
            rooms = Room.objects.filter(max_guests__gte=guests,
                                        pk__in=room_ids_with_availability)
            # Filter by availability rooms
            # Then show the contact form and ready
            bookingForm = BookingForm(request.POST)
            return render(request, 'booking/search_room.html',
                          {'rooms': rooms,
                           'check_in': bookingForm.data.get('check_in'),
                           'check_out': bookingForm.data.get('check_out'),
                           'guests': bookingForm.data.get('guests'),
                           'nights': (check_out - check_in).days,
                           'room_occupation': room_occupation,
                           })
        else:
            return render(request, 'booking/search_room.html',
                          {'bookingDatesForm': bookingDatesForm})
    else:
        bookingDatesForm = BookingDatesForm()
        return render(request, 'booking/search_room.html',
                      {'bookingDatesForm': bookingDatesForm})


def new_booking(request, room_id, check_in, check_out, guests, total_price):
    room = Room.objects.get(pk=room_id)
    if request.method == 'POST':
        bookingForm = BookingForm(request.POST)
        if bookingForm.is_valid():
            bookingForm.save()
            return redirect('home')
        else:
            return render(request, 'booking/new.html',
                          {'room': room,
                           'check_in': check_in,
                           'check_out': check_out,
                           'guests': guests,
                           'total_price': total_price,
                           'bookingForm': bookingForm,
                           })
    else:
        return render(request, 'booking/new.html',
                      {'room': room,
                       'check_in': check_in,
                       'check_out': check_out,
                       'guests': guests,
                       'total_price': total_price,
                       })
