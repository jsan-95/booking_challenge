"""chapp_challenge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

from booking.views import booking_detail, search_room, new_booking
from app.views import home


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home, name='home'),
    path('booking_detail/<int:id>', booking_detail),
    path('search_room', search_room),
    path('new_booking/<int:room_id>/<str:check_in>/<str:check_out>/<str:guests>/<str:total_price>', new_booking,
         name='new_booking'),
]

