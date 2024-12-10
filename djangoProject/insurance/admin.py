from django.contrib import admin
from django import forms
from .models import Carrier, patient, Billing, Invoice

class CarrierAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    search_fields = ('name',)
    ordering = ('name',)

class BillingInline(admin.TabularInline):
    model = Billing
    extra = 1

class PatientAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'insurance_number', 'carrier')
    list_filter = ('carrier',)
    search_fields = ('first_name', 'last_name', 'insurance_number')
    ordering = ('last_name', 'first_name')
    inlines = [BillingInline]

class BillingAdmin(admin.ModelAdmin):
    list_display = ('patient', 'service_description', 'date_of_service', 'amount_billed', 'carrier')
    list_filter = ('carrier', 'patient')
    search_fields = ('service_description', 'patient__first_name', 'patient__last_name')
    ordering = ('date_of_service',)

class InvoiceForm(forms.ModelForm):
    class Meta:
        model = Invoice
        fields = '__all__'
        widgets = {
            'billings': forms.SelectMultiple(attrs={'size': 10}),
        }

class InvoiceAdmin(admin.ModelAdmin):
    form = InvoiceForm
    list_display = ('patient', 'invoice_id', 'amount_paid', 'balance_due', 'payment_status')
    list_filter = ('payment_status',)
    search_fields = ('invoice_id', 'billings__patient__first_name', 'billings__patient__last_name')
    ordering = ('invoice_id',)

    def save_model(self, request, obj, form, change):
        # Save the Invoice instance first to ensure it has an ID
        if not obj.pk:
            super().save_model(request, obj, form, change)

        # After the instance is saved, handle ManyToManyField associations
        form.save_m2m()

        # Recalculate totals after saving the model and associations
        obj.calculate_totals()

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        """
        Filter the available billings based on the selected patient.
        Only show billings related to the selected patient.
        """
        if db_field.name == "billings":
            # Get the selected patient from the request
            patient_id = request.POST.get('patient')
            if patient_id:
                kwargs['queryset'] = Billing.objects.filter(patient_id=patient_id)
        return super().formfield_for_manytomany(db_field, request, **kwargs)

admin.site.register(Carrier, CarrierAdmin)
admin.site.register(patient, PatientAdmin)
admin.site.register(Billing, BillingAdmin)
admin.site.register(Invoice, InvoiceAdmin)
