from django.shortcuts import render, redirect
from django.views import View
from django.utils.timezone import now  # Import the current time utility
from sharedModels.models import Employees, PatientRecord, LabOrders, LabTests
from .forms import viewLabOrders, viewLabTests, AddLabOrderForm, AddLabTestsForm, UpdateLabOrderForm, FilterLabOrdersByPatientForm, FilterLabOrdersByDateOrderedForm, FilterLabOrdersByDatePerformedForm, FilterLabOrdersByPhysicianForm


class labOrder(View):
    def get(self, request):
        # Initialize forms
        view_order_form = viewLabOrders()
        add_order_form = AddLabOrderForm()
        view_test_form = viewLabTests()
        add_test_form = AddLabTestsForm()
        update_lab_form = UpdateLabOrderForm()

        # Filter forms
        filter_patient_form = FilterLabOrdersByPatientForm(request.GET)
        filter_date_ordered_form = FilterLabOrdersByDateOrderedForm(request.GET)
        filter_date_performed_form = FilterLabOrdersByDatePerformedForm(request.GET)
        filter_physician_form = FilterLabOrdersByPhysicianForm(request.GET)

        # Get filter values from the request
        filters = {}
        if filter_patient_form.is_valid():
            patient = filter_patient_form.cleaned_data.get('patient')
            if patient:
                filters['patientid'] = patient

        if filter_date_ordered_form.is_valid():
            date_ordered = filter_date_ordered_form.cleaned_data.get('date_ordered')
            if date_ordered:
                filters['dateordered'] = date_ordered

        if filter_date_performed_form.is_valid():
            date_performed = filter_date_performed_form.cleaned_data.get('date_performed')
            if date_performed:
                filters['dateperfomed'] = date_performed

        if filter_physician_form.is_valid():
            physician = filter_physician_form.cleaned_data.get('physician')
            if physician:
                filters['physicianid'] = physician

        # Apply filters to the LabOrders queryset
        lab_orders = LabOrders.objects.all()
        if filters:
            lab_orders = lab_orders.filter(**filters)

        # Selected Lab Order (view mode)
        selected_order = None
        if request.GET.get('labOrder'):
            selected_order_id = request.GET.get('labOrder')
            selected_order = LabOrders.objects.get(orderid=selected_order_id)

        # Selected Lab Test
        selected_test = None
        if request.GET.get('labTest'):
            selected_test_id = request.GET.get('labTest')
            selected_test = LabTests.objects.get(typeid=selected_test_id)

        return render(request, 'labOrder.html', {
            'view_order_form': view_order_form,
            'add_order_form': add_order_form,
            'update_lab_form': update_lab_form,
            'view_test_form': view_test_form,
            'add_test_form': add_test_form,
            'selected_order': selected_order,
            'selected_test': selected_test,
            # Filter forms
            'filter_patient_form': filter_patient_form,
            'filter_date_ordered_form': filter_date_ordered_form,
            'filter_date_performed_form': filter_date_performed_form,
            'filter_physician_form': filter_physician_form,
            # Filtered lab orders
            'lab_orders': lab_orders,
        })


    def post(self, request):
        # Handle adding a Lab Order
        if 'add_order' in request.POST:
            add_order_form = AddLabOrderForm(request.POST)
            if add_order_form.is_valid():
                LabOrders.objects.create(
                    patientid=add_order_form.cleaned_data['patient'],
                    physicianid=add_order_form.cleaned_data['physician'],
                    teststypeid=add_order_form.cleaned_data['test_type'],
                    technicianid=add_order_form.cleaned_data['lab_technician'],
                    results=-1,
                    dateordered=now(),  # Set the current date and time
                )
                return redirect('labOrder')  # Refresh the page

        # Handle adding a Lab Test
        if 'add_test' in request.POST:
            add_test_form = AddLabTestsForm(request.POST)
            if add_test_form.is_valid():
                LabTests.objects.create(
                    typename=add_test_form.cleaned_data['typename'],
                    normalrange=add_test_form.cleaned_data['normalrange'],
                    urgentrange=add_test_form.cleaned_data['urgentrange'],
                )
                return redirect('labOrder')  # Refresh the page

        # Handle updating a Lab Order
        if 'update_order' in request.POST:
            update_lab_form = UpdateLabOrderForm(request.POST)
            if update_lab_form.is_valid():
                # Retrieve the lab order by its ID
                lab_order_id = request.POST.get('orderid')  # Ensure 'orderid' is passed in the POST request
                lab_order = LabOrders.objects.filter(orderid=lab_order_id).first()  # Safely query for the lab order

                # Update the fields
                lab_order.technicianid = update_lab_form.cleaned_data['lab_technician']
                lab_order.results = update_lab_form.cleaned_data['result']
                lab_order.dateperfomed = now()  # Set the current date and time
                lab_order.save()  # Save changes to the database
                return redirect('labOrder')  # Refresh the page

        # If form is invalid, re-render the page with errors
        view_order_form = viewLabOrders()
        view_test_form = viewLabTests()
        add_order_form = AddLabOrderForm()
        add_test_form = AddLabTestsForm()
        update_lab_form = UpdateLabOrderForm()

        return render(request, 'labOrder.html', {
            'view_order_form': view_order_form,
            'add_order_form': add_order_form,
            'update_lab_form': update_lab_form,
            'view_test_form': view_test_form,
            'add_test_form': add_test_form,
        })
