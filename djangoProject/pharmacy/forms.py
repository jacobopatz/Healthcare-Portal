from django import forms
from .models import Medication
from .models import Prescription

class MedicationForm(forms.ModelForm):
    class Meta:
        model = Medication
        fields = ['medication_name', 'dosage', 'frequency', 'start_date', 'end_date', 'prescribing_doctor']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date'}),
            'end_date': forms.DateInput(attrs={'type': 'date'}),
        }

class PrescriptionForm(forms.ModelForm):
    class Meta:
        model = Prescription
        fields = ['first_name', 'last_name', 'patient_id', 'age',
                  'address', 'city', 'state', 'medication', 'dosage', 'frequency', 
                  'drug_quantity', 'drug_code', 'directions',
                  'date_signed', 'allergies', 'conditions', 'third_party_code', 'signature']
        widgets = {
            'medication': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter medications'}),
            'dosage': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter dosages'}),
            'frequency': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Enter frequencies'}),
            'date_signed': forms.DateInput(attrs={'type': 'date'}),
        }
