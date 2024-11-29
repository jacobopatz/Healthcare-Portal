from . import views
from django.urls import path
from .views import EquipmentView

urlpatterns = [
     path('equipment/',EquipmentView.as_view(),name='equipment'),
     path('equipment/manage/', views.manage_page, name='manage_page'),
]