# In your_project/admin.py
from django.contrib import admin
from .models import Employees  # Adjust the import according to your structure

@admin.register(Employees)
class EmployeesAdmin(admin.ModelAdmin):
    list_display = ('employeeid', 'firstname', 'lastname', 'title', 'phonenumber', 'workdays')
    search_fields = ('firstname', 'lastname', 'title')
