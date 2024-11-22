from django import forms
from sharedModels.models import PatientRecord, Employees, Insurance


class PatientAddForm(forms.ModelForm):
    firstname = forms.CharField(label="First Name", max_length=20)
    lastname = forms.CharField(label="Last Name", max_length=20)
    gender = forms.CharField(label="Gender", max_length=1)
    dob = forms.DateField(label="Date of Birth")
    phonenumber = forms.CharField(label="Phone Number", max_length=15)
    address = forms.CharField(label="Address", max_length=45)
    insuranceid = forms.ModelChoiceField(
        label="Insurance",
        queryset=Insurance.objects.all()
    )
    primaryphysicianid = forms.ModelChoiceField(
        label="Primary Physician",
        queryset=Employees.objects.all())

    class Meta:
        model = PatientRecord
        fields = ['firstname', 'lastname', 'gender', 'dob', 'phonenumber', 'address', 'insuranceid', 'primaryphysicianid']

    changed_time = -1

class PatientSearchForm(forms.Form):
    search_query = forms.CharField(
        label="Search for a patient",
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Search by first name'})
    )
    selected_patient = forms.ModelChoiceField(
        label="Selected Patient",
        queryset=PatientRecord.objects.none(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initially, set the queryset for the 'patient' field to all patients
        self.fields['selected_patient'].queryset = PatientRecord.objects.all()

class PatientEditForm(forms.ModelForm):
    firstname = forms.CharField(label="First Name", max_length=20)
    lastname = forms.CharField(label="Last Name", max_length=20)
    gender = forms.CharField(label="Gender", max_length=1)
    dob = forms.DateField(label="Date of Birth")
    phonenumber = forms.CharField(label="Phone Number", max_length=15)
    address = forms.CharField(label="Address", max_length=45)
    insuranceid = forms.ModelChoiceField(
        label="Insurance",
        queryset=Insurance.objects.all()
    )
    primaryphysicianid = forms.ModelChoiceField(
        label="Primary Physician",
        queryset=Employees.objects.all())

    class Meta:
        model = PatientRecord
        fields = ['patientid', 'firstname', 'lastname', 'gender', 'dob', 'phonenumber', 'address', 'insuranceid', 'primaryphysicianid']

    changed_time = -1




