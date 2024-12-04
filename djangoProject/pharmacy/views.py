from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Prescription, Medication
from .forms import PrescriptionForm, MedicationForm
from django.utils import timezone
from django.contrib import messages

# Existing pharmacy view
class Pharmacy(View):
    def get(self, request):
        return render(request, 'pharmacy.html', {})

# New views for each page
class Prescriptions(View):
    def get(self, request):
        return render(request, 'prescriptions.html', {})

# Add Prescription view
class AddPrescriptionView(View):
    def get(self, request):
        return render(request, 'prescriptions.html')
    
    def post(self, request):
        try:
            first_name = request.POST.get('first_name')
            last_name = request.POST.get('last_name')
            patient_id = request.POST.get('patient_id')
            age = request.POST.get('age')
            date_signed = request.POST.get('date_signed')
            signature = request.POST.get('signature')
            
            # Handling multiple treatment entries
            medications = request.POST.getlist('medication[]')
            dosages = request.POST.getlist('dosage[]')
            frequencies = request.POST.getlist('frequency[]')
            allergies = request.POST.getlist('allergies[]')
            addresses = request.POST.getlist('address[]')
            third_party_code = request.POST.getlist('third_party_code[]')
            conditions = request.POST.getlist('conditions[]')
            drug_quantity = request.POST.getlist('drug_quantity[]')
            drug_code = request.POST.getlist('drug_code[]')
            directions = request.POST.getlist('directions[]')

            # Save each treatment entry in the database
            for medication, dosage, frequency, allergy, address, third_party, condition, quantity, code, direction in zip(
                medications, dosages, frequencies, allergies, addresses, third_party_code, conditions, drug_quantity, drug_code, directions):

                Prescription.objects.create(
                    first_name=first_name,
                    last_name=last_name,
                    patient_id=patient_id,
                    age=age,
                    date_signed=date_signed,
                    signature=signature,
                    medication=medication,
                    dosage=dosage,
                    frequency=frequency,
                    allergies=allergy or "None",  # Default to 'None' if missing
                    addresses=address or "None",  # Default to 'None' if missing
                    third_party_code=third_party or "None",
                    conditions=condition or "None",
                    drug_quantity=quantity or 0,  # Default to 0 if missing
                    drug_code=code or "None",
                    directions=direction or "None",
                    created_at=timezone.now()
                )
            
            return redirect('success_page')  # Redirect to a success page or prescriptions list after submission

        except Exception as e:
            # Handle errors and return the form with an error message
            return HttpResponse(f"An error occurred: {str(e)}")
        
class ViewPrescriptionsView(View):
    def get(self, request):
        prescriptions = Prescription.objects.all()
        return render(request, 'view_prescriptions.html', {'prescriptions': prescriptions})

    def post(self, request):
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        patient_id = request.POST.get('patient_id')

        prescriptions = Prescription.objects.all()

        if first_name:
            prescriptions = prescriptions.filter(first_name__iexact=first_name)
        if last_name:
            prescriptions = prescriptions.filter(last_name__iexact=last_name)
        if patient_id:
            prescriptions = prescriptions.filter(patient_id=patient_id)

        return render(request, 'view_prescriptions.html', {'prescriptions': prescriptions})

def submit_prescription(request):
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('prescriptions')
    else:
        form = PrescriptionForm()
    return render(request, 'prescriptions.html', {'form': form})

class GenerateReportView(View):
    def get(self, request, prescription_id):
        prescription = get_object_or_404(Prescription, pk=prescription_id)
        
        context = {
            'report': {
                'id': prescription_id,
                'hospital_name': "Health Pin Clinic & Services",
                'patient_name': f"{prescription.first_name} {prescription.last_name}",
                'birth_date': prescription.date_signed,
                'allergies': prescription.allergies or "None",
                'address': prescription.address or "Unknown",
                'city': prescription.city or "Unknown",
                'state': prescription.state or "Unknown",
                'third_party_code': prescription.third_party_code or "N/A",
                'conditions': prescription.conditions or "None",
                'status': "Active", 
                'drug_quantity': prescription.drug_quantity or 0,
                'dosage': prescription.dosage or "N/A",
                'date_issued': prescription.date_signed,
                'drug_code': prescription.drug_code or "N/A",
                'directions': prescription.directions or "No directions provided",
            }
        }
        return render(request, 'summary_report.html', context)

def generate_report(request):
    prescriptions = Prescription.objects.all()
    return render(request, 'summary_report_all.html', {'prescriptions': prescriptions})

class ManageMedicationsView(View):
    def get(self, request):
        return render(request, 'manage_medications.html')
    
def manage_medications(request):
    return render(request, 'pharmacy/manage_medications.html')

class AddMedicationView(View):
    def get(self, request):
        form = MedicationForm()
        return render(request, 'add_medication.html', {'form': form})

    def post(self, request):
        form = MedicationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Medication added successfully!")
            return redirect('view_medications')
        else:
            messages.error(request, "Error adding medication. Please check the form and try again.")
        return render(request, 'add_medication.html', {'form': form})

class ViewMedicationsView(View):
    def get(self, request):
        query = request.GET.get('search', '')
        condition1 = request.GET.get('condition1', '')
        condition2 = request.GET.get('condition2', '')
        med_type = request.GET.get('med_type', '')
        
        medications = Medication.objects.all()

        if query:
            medications = medications.filter(medication_name__icontains=query)
        if condition1:
            medications = medications.filter(description__icontains=condition1)
        if condition2:
            medications = medications.filter(description__icontains=condition2)
        if med_type:
            medications = medications.filter(description__icontains=med_type)

        return render(request, 'view_medications.html', {
            'medications': medications,
            'search_query': query,
            'condition1': condition1,
            'condition2': condition2,
            'med_type': med_type,
        })
    
class Medications(View):
    def get(self, request):
        return render(request, 'medications.html', {})
    
def edit_medication(request, id):
    medication = get_object_or_404(Medication, id=id)
    if request.method == "POST":
        form = MedicationForm(request.POST, instance=medication)
        if form.is_valid():
            form.save()
            return redirect('view_medications')
    else:
        form = MedicationForm(instance=medication)
    return render(request, 'pharmacy/edit_medication.html', {'form': form})

class Help(View):
    def get(self, request):
        return render(request, 'help.html', {})

def delete_medication(request, id):
    medication = get_object_or_404(Medication, id=id)
    if request.method == "POST":
        medication.delete()
        return redirect('view_medications')
    return render(request, 'pharmacy/delete_medication_confirm.html', {'medication': medication})

def help_page(request):
    return render(request, 'help.html')

def faq_page(request):
    return render(request, 'faq.html')

def contact_support_page(request):
    return render(request, 'contact_support.html')

def send_support_ticket(request):
    if request.method == "POST":
        subject = request.POST.get('subject')
        reason = request.POST.get('reason')
        return HttpResponse(f"Support ticket received: {subject}")
    return HttpResponse("Invalid request method.")
