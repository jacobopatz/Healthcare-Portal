from django.shortcuts import render
from django.http import JsonResponse
from django.db.models import Q
from .models import patient, Billing, Invoice

def insurance_billing_management(request):
    # Check if this is an AJAX request for autocomplete
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' and request.method == 'GET':
        query = request.GET.get('q', '').strip()
        if query:
            # Filter patients by first name, last name, or insurance number
            patients = patient.objects.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(insurance_number__icontains=query)
            )
            # Return matching patient data as JSON
            results = [
                {
                    'id': patient_obj.id,
                    'first_name': patient_obj.first_name,
                    'last_name': patient_obj.last_name,
                    'insurance_number': patient_obj.insurance_number
                }
                for patient_obj in patients
            ]
            return JsonResponse(results, safe=False)
        return JsonResponse([], safe=False)

    # Handle normal search requests
    query = request.GET.get('q', '').strip()
    if query:
        # Filter patients by name or insurance number
        patients = patient.objects.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(insurance_number__icontains=query)
        )
    else:
        # If no search term, display all patients
        patients = patient.objects.all()

    # Prefetch related billings and invoices for each patient
    patients = patients.prefetch_related('billings', 'billings__invoices', 'carrier')

    # Prepare structured data to send to the template
    patients_data = []
    for patient_obj in patients:
        patient_data = {
            'id': patient_obj.id,
            'first_name': patient_obj.first_name,
            'last_name': patient_obj.last_name,
            'insurance_number': patient_obj.insurance_number,
            'carrier': {
                'name': patient_obj.carrier.name,
                'address': patient_obj.carrier.address,
                'phone': patient_obj.carrier.phone
            },
            'billings': [
                {
                    'service_id': billing.service_id,
                    'service_description': billing.service_description,
                    'date_of_service': billing.date_of_service,
                    'amount_billed': billing.amount_billed,
                    'carrier': {
                        'name': billing.carrier.name
                    },
                    'invoices': [
                        {
                            'invoice_id': invoice.invoice_id,
                            'total_amount': invoice.total_amount,
                            'amount_paid': invoice.amount_paid,
                            'balance_due': invoice.balance_due,
                            'payment_status': invoice.payment_status
                        }
                        for invoice in billing.invoices.all()
                    ]
                }
                for billing in patient_obj.billings.all()
            ]
        }
        patients_data.append(patient_data)

    # Pass structured data to the template
    return render(request, 'insurance.html', {
        'patients_json': patients_data,
        'query': query
    })
