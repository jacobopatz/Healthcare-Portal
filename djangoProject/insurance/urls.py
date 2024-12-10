from . import views
from django.urls import path
from .views import insurance_billing_management

urlpatterns = [
     path('insurance/',insurance_billing_management,name='insurance'),

]
