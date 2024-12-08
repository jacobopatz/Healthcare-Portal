import json
from django.shortcuts import render
from .models import Patient, Billing
from datetime import date

def patient_billing_view(request):
    patients = Patient.objects.all()

    patients_data = []
    for patient in patients:
        patient_data = {
            'id': patient.id,
            'first_name': patient.first_name,
            'last_name': patient.last_name,
            'dob': patient.date_of_birth.strftime('%Y-%m-%d'), 
            'insurance_number': patient.insurance_number,
            'carrier_name': patient.carrier.name if patient.carrier else None,  
            'billings': [
                {
                    'invoice_number': billing.invoice_number,
                    'invoice_date': billing.invoice_date.strftime('%Y-%m-%d'),
                    'service_description': billing.service_description,  
                    'total_amount': str(billing.total_amount)  
                }
                for billing in Billing.objects.filter(patient=patient)
            ]
        }
        patients_data.append(patient_data)

    return render(request, 'insurance.html', {
        'patients_json': json.dumps(patients_data) 
    })
