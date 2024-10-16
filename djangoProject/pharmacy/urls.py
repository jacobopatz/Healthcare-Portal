from . import views
from django.urls import path

urlpatterns = [
     path('pharmacy/',views.pharmacy.as_view(),name='pharmacy'),
]