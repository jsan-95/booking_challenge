from datetime import datetime, date

from django.forms import EmailInput, ModelForm

from booking.models import Booking


class BookingForm(ModelForm):

    def clean(self):
        cleaned_data = super(BookingForm, self).clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        if check_in and check_out:
            if check_out <= check_in:
                self._errors['check_out'] = self.error_class([
                    'La fecha de salida debe ser posterior a la fecha de '
                    'entrada'])
            if check_in < datetime.date.today():
                self._errors['check_out'] = self.error_class([
                    'La fecha de entrada debe ser posterior a hoy'])

        room = cleaned_data.get('room')
        if room:
            cleaned_data['total_price'] = room.price * (check_out - check_in).days

        return cleaned_data

    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'guests', 'room', 'name',
                  'email', 'phone', 'total_price']
        widgets = {
            'email': EmailInput(attrs={'type': 'email'})
        }

        error_messages = {
            'check_in': {
                'required': "Introduce la fecha de entrada",
            },
            'check_out': {
                'required': "Introduce la fecha de salida",
            },
            'guests': {
                'required': "Introduce el número de huéspedes",
            },
            'room': {
                'required': "Introduce la habitación",
            },
            'name': {
                'required': "Introduce tu nombre",
            },
            'email': {
                'required': "Introduce tu email",
            },
            'phone': {
                'required': "Introduce tu número de teléfono",
            }
        }


class BookingDatesForm(ModelForm):

    def clean(self):
        cleaned_data = super(BookingDatesForm, self).clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')
        if check_in and check_out:
            if check_out <= check_in:
                self._errors['check_out'] = self.error_class([
                    'La fecha de salida debe ser posterior a la fecha de '
                    'entrada'])
            if check_in < date.today():
                self._errors['check_out'] = self.error_class([
                    'La fecha de entrada debe ser posterior a hoy'])

            last_day_of_current_year = date(date.today().year, 12, 31)


            if check_out > last_day_of_current_year:
                self._errors['check_out'] = self.error_class([
                    'La fecha de salida debe ser antes de fin de año'])

        return cleaned_data

    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'guests']

        error_messages = {
            'check_in': {
                'required': "Introduce la fecha de entrada",
            },
            'check_out': {
                'required': "Introduce la fecha de salida",
            },
        }


class BookingSearchRoomForm(ModelForm):

    class Meta:
        model = Booking
        fields = ['check_in', 'check_out', 'guests', 'room', 'total_price']
