from . import views
from django.urls import path

urlpatterns = [
     path('patientRecord/',views.patientRecord.as_view(),name='patientRecord'),
]