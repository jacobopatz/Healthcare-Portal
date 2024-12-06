from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Patient, Billing

class PatientAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'date_of_birth', 'insurance_number', 'carrier_name']

class BillingAdmin(admin.ModelAdmin):
    list_display = ['invoice_number', 'invoice_date', 'service_description', 'total_billed', 'patient']
# Register your models here
admin.site.register(Patient)
admin.site.register(Billing)