from . import views
from django.urls import path

urlpatterns = [
     path('equipment/',views.equipment.as_view(),name='equipment'),
]