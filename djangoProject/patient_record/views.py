from django.shortcuts import render
from django.views import View
from sharedModels.models import Employees, PatientRecord, Insurance
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PatientAddForm, PatientSearchForm, PatientEditForm

# Create your views here.
class PatientRecordView(View):

    def get(self, request):

        # Add Patient section
        add_form = PatientAddForm()

        # Search Patient section
        search_form = PatientSearchForm(request.GET or None)
        selected_patient = None
        selected_patient_id = None
        edit_mode = False

        if request.GET and search_form.is_valid():
            search_query = search_form.cleaned_data.get('search_query', '')

            if search_query:
                patients = PatientRecord.objects.filter(firstname__icontains=search_query)
                search_form.fields['selected_patient'].queryset = patients
            else:
                search_form.fields['selected_patient'].queryset = PatientRecord.objects.all()

            selected_patient = search_form.cleaned_data.get('selected_patient')
            selected_patient_id = selected_patient.patientid if selected_patient else None

        return render(request, 'PatientRecord.html', {
            'add_form': add_form,
            'search_form': search_form,
            'selected_patient': selected_patient,
            'selected_patient_id': selected_patient_id,
            'edit_mode': edit_mode,
            'insurances': Insurance.objects.all(),
            'physicians': Employees.objects.all()
        })

    def post(self, request):
        # Forms for adding and searching
        add_form = PatientAddForm()
        search_form = PatientSearchForm()

        edit_form = None
        edit_mode = request.POST.get('edit_mode') == 'True'
        selected_patient_id = request.POST.get('selected_patient_id')
        selected_patient = None

        print(f"Edit Mode: {edit_mode}")
        print(f"Selected Patient ID: {selected_patient_id}")

        # Retrieve the selected patient
        if selected_patient_id:
            try:
                selected_patient = PatientRecord.objects.get(patientid=selected_patient_id)
                print(f"Selected Patient: {selected_patient}")
                edit_form = PatientEditForm(instance=selected_patient)
                # print(f"Edit form: {edit_form} {edit_form.lastname}")
            except PatientRecord.DoesNotExist:
                print("No patient found with the given ID.")
                selected_patient = None
        else:
            print("No patient id")


        # Handle saving changes
        if request.POST.get('save_changes') and edit_form:
            print("Save changes button pressed")
            print(f"Now selected patient is {selected_patient}")
            # print(edit_form)

            edit_form = PatientEditForm(request.POST, instance=selected_patient)
            if edit_form:
                edit_form.save()
                print("Patient updated successfully.")
                edit_mode = False  # Exit edit mode
            else:
                print(f"Edit form errors: {edit_form.errors}")

        # Handle Adding a New Patient
        add_form = PatientAddForm(request.POST)
        if request.POST.get('add_patient') and add_form.is_valid():
            add_form.save()
            print("New patient added successfully.")

        # Render the template with the context
        return render(request, 'PatientRecord.html', {
            'add_form': add_form,
            'search_form': search_form,
            'edit_form': edit_form,
            'selected_patient': selected_patient,
            'selected_patient_id': selected_patient_id,
            'edit_mode': edit_mode,
            'insurances': Insurance.objects.all(),
            'physicians': Employees.objects.all(),
    })

