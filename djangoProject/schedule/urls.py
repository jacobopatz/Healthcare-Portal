from . import views
from django.urls import path
from .views import ScheduleView, findPhysicianView, cancel_appointment
from django.db import models
import uuid


urlpatterns = [
     path('schedule/', ScheduleView.as_view(), name='schedule'),
     path('schedule/makeAppointment/',findPhysicianView.as_view(),name='findPhysician'),
     path('schedule/cancel_appointment/<uuid:appt_id>', cancel_appointment, name='cancel_appointment'),
     # path('BookAppointment/',BookingView.as_view(), name ='booking')
]