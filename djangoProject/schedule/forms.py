from django import forms
from sharedModels.models import Employees,PatientRecord, Appointments

class PhysicianSelectionForm(forms.Form):
    physician = forms.ModelChoiceField(
        queryset=Employees.objects.all(),  # Ensure you fetch all employees here
        label='Select Physician'
    )
    
    changed_time = -1


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointments
        fields = ['date', 'enddate', 'physcianid','aptType','description','patientid']  # Include other fields you want
    

class viewPhysicianForm(forms.Form):
    physician = forms.ModelChoiceField(
        queryset=Employees.objects.all(),  # Ensure you fetch all employees here
        label=''
    )

    

