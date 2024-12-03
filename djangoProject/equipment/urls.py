from . import views
from django.urls import path
from .views import EquipmentView, ManageView, ProblemsView, AddProblemView

urlpatterns = [
     path('equipment/',EquipmentView.as_view(),name='equipment'),
     path('equipment/manage/', ManageView.as_view(),name='manage_page'),
     path('equipment/problems/', ProblemsView.as_view(),name='problems_page'),
     path('equipment/problems/addProblem', AddProblemView.as_view(),name="'add_problem")
]