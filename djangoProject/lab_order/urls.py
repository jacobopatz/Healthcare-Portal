from .views import labOrder
from django.urls import path

urlpatterns = [
     path('labOrder/',labOrder.as_view(),name='labOrder')
]