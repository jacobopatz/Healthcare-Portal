from . import views
from django.urls import path

urlpatterns = [
     path('insurance/',views.insurance.as_view(),name='insurance'),
]