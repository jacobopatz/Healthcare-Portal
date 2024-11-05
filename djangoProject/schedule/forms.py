from django import forms
from sharedModels.models import Employees,PatientRecord

class PhysicianSelectionForm(forms.Form):
    physician = forms.ModelChoiceField(
        queryset=Employees.objects.all(),  # Ensure you fetch all employees here
        label='Select Physician'
    )
    patient = forms.ModelChoiceField(
        queryset = PatientRecord.objects.all(),
        label='Select Patient'
    )
