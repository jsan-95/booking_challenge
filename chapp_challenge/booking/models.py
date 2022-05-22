import uuid

import django
from django.db import models


class Room(models.Model):
    name = models.CharField(max_length=255)
    price = models.FloatField()
    max_guests = models.IntegerField()
    max_availability = models.IntegerField()

    def __str__(self):
        return f'Habitación {self.name.lower()}'


class Booking(models.Model):
    check_in = models.DateField(max_length=255,
                                default=django.utils.timezone.now)
    check_out = models.DateField(max_length=255,
                                 default=django.utils.timezone.now)
    room = models.ForeignKey(Room, on_delete=models.SET_NULL, null=True)
    guests = models.IntegerField()
    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    total_price = models.FloatField()
    locator = models.UUIDField(default=uuid.uuid4, editable=False)

    def __str__(self):
        return f'Reserva {self.locator}: {self.name}'

    @property
    def nights(self):
        return (self.check_out - self.check_in).days
