from . import views
from django.urls import path
from .views import EquipmentView, VendorView, ManageView, ProblemsView, AddProblemType, DepartmentView

urlpatterns = [
     path('equipment/',EquipmentView.as_view(),name='equipment'),
     path('equipment/vendor/', VendorView.as_view(),name='vendor_search'),
     path('equipment/department/', DepartmentView.as_view(),name='department_search'),
     path('equipment/manage/', ManageView.as_view(),name='manage_page'),
     path('equipment/problems/', ProblemsView.as_view(),name='problems_page'),
     path('equipment/problems/addProblem', AddProblemType.as_view(),name='add_problem')
]