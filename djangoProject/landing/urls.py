from . import views
from django.urls import path

urlpatterns = [
     path('landing/',views.landing.as_view(),name='landing'),
]