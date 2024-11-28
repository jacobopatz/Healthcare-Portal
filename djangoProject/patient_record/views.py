from django.shortcuts import render
from django.views import View
from sharedModels.models import Employees, PatientRecord, Encounters, Insurance, LabOrders, PharmacyOrder
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PatientAddForm, PatientSearchForm, PatientEditForm, EncounterAddForm, EncounterSearchForm

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
        add_form = PatientAddForm(request.POST)
        search_form = PatientSearchForm()

        # Form and other variables needed for editing
        edit_form = None
        edit_mode = request.POST.get('edit_mode') == 'True'
        selected_patient_id = request.POST.get('selected_patient_id')
        selected_patient = None

        # Debug code
        print(f"Edit Mode: {edit_mode}")
        print(f"Selected Patient ID: {selected_patient_id}")

        # Add Patient Code
        if request.POST.get('add_patient') and add_form.is_valid():
            add_form.save()
            print("New patient added successfully.")

        # View Record Code

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


        # Edit a patient and save
        if request.POST.get('save_changes') and edit_form:
            print("Save changes button pressed")
            print(f"Now selected patient is {selected_patient}")
            # print(edit_form)

            edit_form = PatientEditForm(request.POST, instance=selected_patient)
            if edit_form.is_valid():
                edit_form.save()
                print("Patient updated successfully.")
                edit_mode = False  # Exit edit mode
            else:
                print(f"Edit form errors: {edit_form.errors}")

        # Remove a patient
        if request.POST.get('delete') and edit_form:
            print("Delete button pressed")
            PatientRecord.objects.filter(patientid=selected_patient_id).delete()
            selected_patient = None



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


class EncounterRecordView(View):

    def get(self, request):

        # Add Encounter section
        add_form = EncounterAddForm()

        # Search Encounter section
        search_form = EncounterSearchForm(request.GET or None)
        selected_encounter = None
        selected_encounter_id = None
        edit_mode = False

        if request.GET and search_form.is_valid():
            search_query = search_form.cleaned_data.get('search_query', '')

            if search_query:
                encounters = Encounters.objects.filter(date__icontains=search_query)
                search_form.fields['selected_encounter'].queryset = encounters
            else:
                search_form.fields['selected_encounter'].queryset = Encounters.objects.all()

            selected_encounter = search_form.cleaned_data.get('selected_encounter')
            selected_encounter_id = selected_encounter.encounterid if selected_encounter else None


        return render(request, 'EncounterRecord.html', {
            'add_form': add_form,
            'search_form': search_form,
            'selected_encounter': selected_encounter,
            'selected_encounter_id': selected_encounter_id,
            'physicians': Employees.objects.all(),
            'patients': PatientRecord.objects.all(),
            'laborders': LabOrders.objects.all(),
            'pharmacyorders': PharmacyOrder.objects.all(),
        })

    def post(self, request):

        #Forms for adding and searching
        add_form = EncounterAddForm(request.POST)
        search_form = EncounterSearchForm()

        # Form and other variables needed for editing
        edit_form = None
        edit_mode = request.POST.get('edit_mode') == 'True'
        selected_encounter_id = request.POST.get('selected_encounter_id')
        selected_encounter = None


        # Add Encounter Code
        if request.POST.get('add_encounter') and add_form.is_valid():
            add_form.save()
            print("New encounter successfully.")
        else:
            print("Encounter could not be added")
            print(add_form.errors)

        # Retrieve the selected encounter
        if selected_encounter_id:
            try:
                selected_encounter = Encounters.objects.get(encounterid=selected_encounter_id)
                print(f"Selected Encounter: {selected_encounter}")
                edit_form = EncounterAddForm(instance=selected_encounter)
                # print(f"Edit form: {edit_form} {edit_form.lastname}")
            except Encounters.DoesNotExist:
                print("No patient found with the given ID.")
                selected_encounter = None
        else:
            print("No encounter id")

        # Edit a patient and save
        if request.POST.get('save_changes') and edit_form:
            print("Save changes button pressed")
            print(f"Now selected patient is {selected_encounter}")
            # print(edit_form)

            edit_form = EncounterAddForm(request.POST, instance=selected_encounter)
            if edit_form.is_valid():
                edit_form.save()
                print("Patient updated successfully.")
                edit_mode = False  # Exit edit mode
            else:
                print(f"Edit form errors: {edit_form.errors}")

        # Remove a patient
        if request.POST.get('delete') and edit_form:
            print("Delete button pressed")
            Encounters.objects.filter(encounterid=selected_encounter_id).delete()
            selected_encounter = None

        # Render the template with the context
        return render(request, 'EncounterRecord.html', {
            'add_form': add_form,
            'search_form': search_form,
            'edit_form': edit_form,
            'selected_encounter': selected_encounter,
            'selected_encounter_id': selected_encounter_id,
            'edit_mode': edit_mode,
            'physicians': Employees.objects.all(),
            'patients': PatientRecord.objects.all(),
            'laborders': LabOrders.objects.all(),
            'pharmacyorders': PharmacyOrder.objects.all(),
        })

