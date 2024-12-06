from django import forms
from sharedModels.models import Employees,PatientRecord, LabOrders, LabTests

class viewLabOrders(forms.Form):
    labOrder = forms.ModelChoiceField(
        queryset=  LabOrders.objects.all(),
        label='Select Lab Orders'
    )
    

class viewLabTests(forms.Form):
    labTest = forms.ModelChoiceField(
        queryset= LabTests.objects.all(),
        label='Select Lab Tests'
    )

class AddLabOrderForm(forms.Form):
    patient = forms.ModelChoiceField(
        queryset=PatientRecord.objects.all(),
        label="Patient Name"
    )
    physician = forms.ModelChoiceField(
        queryset=Employees.objects.all(), #filter(title="physician"),
        label="Physician Name"
    )
    test_type = forms.ModelChoiceField(
        queryset=LabTests.objects.all(),
        label="Type of Lab Test"
    )
    lab_technician = forms.ModelChoiceField(
        queryset=Employees.objects.all(),    #filter(title="labTechnician"),
        label="Lab Technician"
    )


class UpdateLabOrderForm(forms.Form):
    labTest = forms.ModelChoiceField(
        queryset= LabOrders.objects.all(),
        label='Select Lab Tests'
    )

    result = forms.CharField(
        max_length=10,
        label="Result",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

    lab_technician = forms.ModelChoiceField(
        queryset=Employees.objects.all(),    #filter(title="labTechnician"),
        label="Lab Technician"
    )

class AddLabTestsForm(forms.Form):
    typename = forms.CharField(
        max_length=20,
        label="Test Name",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    normalrange = forms.CharField(
        max_length=10,
        label="Normal Range",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )
    urgentrange = forms.CharField(
        max_length=10,
        label="Urgent Range",
        widget=forms.TextInput(attrs={'class': 'form-control'}),
    )

class FilterLabOrdersByPatientForm(forms.Form):
    patient = forms.ModelChoiceField(
        queryset=PatientRecord.objects.all(),
        label="Patient Name",
        required=False
    )

class FilterLabOrdersByDateOrderedForm(forms.Form):
    date_ordered = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date Ordered",
        required=False
    )

class FilterLabOrdersByDatePerformedForm(forms.Form):
    date_performed = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        label="Date Performed",
        required=False
    )

class FilterLabOrdersByPhysicianForm(forms.Form):
    physician = forms.ModelChoiceField(
        queryset=Employees.objects.filter(title="physician"),
        label="Physician Name",
        required=False
    )

