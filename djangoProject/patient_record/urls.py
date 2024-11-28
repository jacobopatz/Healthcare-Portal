from . import views
from django.urls import path

urlpatterns = [
     path('patientRecord/',views.PatientRecordView.as_view(),name='patientRecord'),
     path('encounterRecord/',views.EncounterRecordView.as_view(),name='encounterRecord')
]