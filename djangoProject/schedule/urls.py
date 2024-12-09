from . import views
from django.urls import path
from .views import ScheduleView, findPhysicianView,popUpView


urlpatterns = [
     path('schedule/', ScheduleView.as_view(), name='schedule'),
     path('schedule/makeAppointment/',findPhysicianView.as_view(),name='findPhysician'),
     path('schedule/popUp/',popUpView.as_view(), name='popUp')
     # path('BookAppointment/',BookingView.as_view(), name ='booking')
]