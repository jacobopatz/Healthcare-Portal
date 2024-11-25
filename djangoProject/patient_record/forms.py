from django import forms
from sharedModels.models import PatientRecord, Encounters, Employees, Insurance, LabOrders, LabTests, PharmacyOrder


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


class EncounterAddForm(forms.ModelForm):
    date = forms.DateTimeField(label='Date')
    physicianid = forms.ModelChoiceField(
        label="Physician",
        queryset=Employees.objects.all()
    )
    patientid = forms.ModelChoiceField(
        label="Patient",
        queryset=PatientRecord.objects.all()
    )
    patientcomplaints = forms.CharField(label='Patient Complaints', max_length=120, required=False)
    vitalsigns = forms.CharField(label='Vital Signs', max_length=120, required=False)
    practitionernotes = forms.CharField(label='PractitionerNotes', max_length=120, required=False)
    laborderid = forms.ModelChoiceField(
        label="Lab Order",
        queryset=LabOrders.objects.all(),
        required=False
    )
    pharmacyorderid = forms.ModelChoiceField(
        label="Pharmacy Order",
        queryset=LabOrders.objects.all(),
        required=False
    )
    treatment_plan = forms.CharField(label='Treatment Plan', max_length=120, required=False)
    refferals = forms.CharField(label='Referrals', max_length=120, required=False)
    recfollowup = forms.DateField(label='RecFollowUp', required=False)

    class Meta:
        model = Encounters
        fields = ['date', 'physicianid', 'patientid', 'patientcomplaints', 'practitionernotes', 'vitalsigns', 'laborderid', 'pharmacyorderid', 'treatment_plan', 'refferals', 'recfollowup' ]

class EncounterSearchForm(forms.Form):
    search_query = forms.CharField(
        label="Search for an encounter",
        max_length=100,
        required=False,
        widget=forms.DateInput(attrs={'placeholder': 'Search by date'})
    )
    selected_encounter = forms.ModelChoiceField(
        label="Selected Encounter",
        queryset=Encounters.objects.none(),
        required=False
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Initially, set the queryset for the 'patient' field to all patients
        self.fields['selected_encounter'].queryset = Encounters.objects.all()


