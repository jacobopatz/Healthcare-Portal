from . import views
from django.urls import path
from .views import patient_billing_view

urlpatterns = [
     path('insurance/',patient_billing_view,name='insurance'),
]
