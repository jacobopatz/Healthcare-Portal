# your_app/admin.py
from django.contrib import admin
from .models import Employees, Appointments, Encounters, Equipment, Insurance, Invoice, LabOrders, LabTests, Maintenance, Medication, PatientRecord, PharmacyOrder, Services, Users

# Register your models here.
admin.site.register(Employees)
admin.site.register(Appointments)
admin.site.register(Encounters)
admin.site.register(Equipment)
admin.site.register(Insurance)
admin.site.register(Invoice)
admin.site.register(LabOrders)
admin.site.register(LabTests)
admin.site.register(Maintenance)
admin.site.register(Medication)
admin.site.register(PatientRecord)
admin.site.register(PharmacyOrder)
admin.site.register(Services)
admin.site.register(Users)