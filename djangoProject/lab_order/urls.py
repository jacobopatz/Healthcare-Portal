from .views import labOrder
from django.urls import path

urlpatterns = [
     path('LabOrder/',labOrder.as_view(),name='labOrder')
]