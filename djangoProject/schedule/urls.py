from . import views
from django.urls import path
from .views import ScheduleView, findPhysicianView


urlpatterns = [
     path('schedule/', ScheduleView.as_view(), name='schedule'),
     path('schedule/makeAppointment/',findPhysicianView.as_view(),name='findPhysician')
     # path('BookAppointment/',BookingView.as_view(), name ='booking')
]