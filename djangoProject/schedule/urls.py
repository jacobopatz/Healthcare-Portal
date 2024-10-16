from . import views
from django.urls import path


urlpatterns = [
     path('schedule/',views.schedule.as_view(),name='schedule'),
]