from . import views
from django.urls import path

urlpatterns = [
     path('patientRecord/',views.PatientRecordView.as_view(),name='patientRecord'),
]