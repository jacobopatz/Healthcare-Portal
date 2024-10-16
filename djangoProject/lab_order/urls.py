from . import views
from django.urls import path

urlpatterns = [
     path('labOrder/',views.labOrder.as_view(),name='labOrder'),
]