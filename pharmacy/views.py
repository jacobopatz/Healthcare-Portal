from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Prescription, SummaryReport, Medication
from .forms import PrescriptionForm, MedicationForm
from django.utils import timezone
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from django.db.models import Q

# Existing pharmacy view
class Pharmacy(View):
    def get(self, request):
        return render(request, 'pharmacy.html', {})

# New views for each page
class Prescriptions(View):
    def get(self, request):
        return render(request, 'prescriptions.html', {})
    
# This is a sample view for handling the Add Prescription Form page
class AddPrescriptionView(View):
    def get(self, request):
        # Display the form page
        return render(request, 'prescriptions.html')
    
    def post(self, request):
        # Handle form submission
        # Assuming that 'Prescription' is a model in models.py with fields
        # that correspond to the form fields (e.g., first_name, last_name, etc.)
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
            
            # Save each treatment entry in the database
            for medication, dosage, frequency in zip(medications, dosages, frequencies):
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
                    created_at=timezone.now()
                )
                
            return redirect('success_page')  # Redirect to a success page or prescriptions list after submission

        except Exception as e:
            # Handle errors and return the form with an error message
            return HttpResponse(f"An error occurred: {str(e)}")
        
class ViewPrescriptionsView(View):
    def get(self, request):
        # Display an empty list on initial load or optionally some recent entries
        prescriptions = Prescription.objects.none()  # Start with an empty queryset
        return render(request, 'view_prescriptions.html', {'prescriptions': prescriptions})

    def post(self, request):
        # Retrieve form inputs
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        patient_id = request.POST.get('patient_id', '').strip()

        # Build a dynamic query using Q objects
        query = Q()
        if first_name:
            query &= Q(patient__first_name__iexact=first_name)
        if last_name:
            query &= Q(patient__last_name__iexact=last_name)
        if patient_id:
            query &= Q(patient__id=patient_id)

        # Execute the query
        prescriptions = Prescription.objects.filter(query)

        # Render the filtered results
        return render(request, 'view_prescriptions.html', {'prescriptions': prescriptions})

def submit_prescription(request):
    if request.method == "POST":
        form = PrescriptionForm(request.POST)
        if form.is_valid():
            form.save()  # Save the prescription
            return redirect('prescriptions')  # Redirect to prescriptions page or another page
    else:
        form = PrescriptionForm()
    return render(request, 'prescriptions.html', {'form': form})

# Generate report for all prescriptions
def generate_report(request):
    prescriptions = Prescription.objects.all()  # Replace with filtering logic if needed

    # Pass data to the summary report template
    return render(request, 'summary_report.html', {
        'prescriptions': prescriptions
    })

def summary_report_view(request, report_id):
    report = get_object_or_404(SummaryReport, id=report_id)
    context = {'report': report}
    return render(request, 'summary_report.html', context)

def export_pdf_view(request, report_id):
    report = get_object_or_404(SummaryReport, id=report_id)
    template_path = 'summary_report_pdf.html'
    context = {'report': report}
    
    # Render the template to an HTML string
    template = get_template(template_path)
    html = template.render(context)
    
    # Create a PDF from the HTML string
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="SummaryReport_{report_id}.pdf"'
    
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors with the PDF generation")
    
    return response

# Export report as PDF
def export_pdf(request):
    prescriptions = Prescription.objects.all()  # Replace with actual filtering logic
    template_path = 'summary_report_pdf.html'
    context = {'prescriptions': prescriptions}
    
    # Render the template to an HTML string
    template = get_template(template_path)
    html = template.render(context)
    
    # Create a PDF from the HTML string
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Prescription_Summary.pdf"'
    
    # Generate PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("We had some errors with the PDF generation")
    
    return response

class ManageMedicationsView(View):
    def get(self, request):
        return render(request, 'manage_medications.html')
    
def manage_medications(request):
    return render(request, 'pharmacy/manage_medications.html')

class AddMedicationView(View):
    def get(self, request):
        # Render an empty form for adding medication
        form = MedicationForm()
        return render(request, 'add_medication.html', {'form': form})

    def post(self, request):
        # Handle form submission
        form = MedicationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the medication record to the database
            messages.success(request, "Medication added successfully!")
            return redirect('view_medications')  # Redirect to the view medications page
        else:
            messages.error(request, "Error adding medication. Please check the form and try again.")
        return render(request, 'add_medication.html', {'form': form})


class ViewMedicationsView(View):
    def get(self, request):
        # Retrieve filter and search parameters from the GET request
        query = request.GET.get('search', '')
        condition1 = request.GET.get('condition1', '')
        condition2 = request.GET.get('condition2', '')
        med_type = request.GET.get('med_type', '')
        
        # Fetch all medications
        medications = Medication.objects.all()

        # Apply search filters dynamically
        if query:
            medications = medications.filter(medication_name__icontains=query)
        if condition1:
            medications = medications.filter(description__icontains=condition1)  # Adjust condition field name
        if condition2:
            medications = medications.filter(description__icontains=condition2)  # Adjust condition field name
        if med_type:
            medications = medications.filter(description__icontains=med_type)  # Use 'description' for med_type

        # Pass medications to the template for display
        return render(request, 'view_medications.html', {
            'medications': medications,
            'search_query': query,   # Pass the current search query back to the template
            'condition1': condition1,  # Pass selected filters to the template
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
            return redirect('view_medications')  # Redirect to the medication list or other page
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
        return redirect('view_medications')  # Redirect to medication list or another page
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
        # Handle the data (e.g., save to database, send email, etc.)
        return HttpResponse(f"Support ticket received: {subject}")
    return HttpResponse("Invalid request method.")