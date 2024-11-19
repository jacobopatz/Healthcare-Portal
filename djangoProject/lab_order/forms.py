from django import forms
from sharedModels.models import Employees,PatientRecord, LabOrders, LabTests

class viewLabOrders(forms.Form):
    labOrder = forms.ModelChoiceField(
        queryset=  LabOrders.objects.all(),
        label='Select Lab Orders'
    )

class viewLabTests(forms.Form):
    labOrder = forms.ModelChoiceField(
        queryset= LabTests.objects.all(),
        label='Select Lab Tests'
    )

class AddLabOrderForm(forms.Form):
    patient = forms.ModelChoiceField(
        queryset=PatientRecord.objects.all(),
        label="Patient Name"
    )
    physician = forms.ModelChoiceField(
        queryset=Employees.objects.all(),
        label="Physician Name"
    )
    test_type = forms.ModelChoiceField(
        queryset=LabTests.objects.all(),
        label="Type of Lab Test"
    )
    lab_technician = forms.ModelChoiceField(
        queryset=Employees.objects.all(),
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