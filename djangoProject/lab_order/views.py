from django.shortcuts import render, redirect
from django.views import View
from sharedModels.models import Employees, PatientRecord, LabOrders, LabTests
from .forms import viewLabOrders, viewLabTests, AddLabOrderForm, AddLabTestsForm


class labOrder(View):
    def get(self, request):
        # Forms
        view_order_form = viewLabOrders()
        add_order_form = AddLabOrderForm()
        view_test_form = viewLabTests()
        add_test_form = AddLabTestsForm()

        # Selected Lab Order
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
            'view_test_form': view_test_form,
            'add_test_form': add_test_form,
            'selected_order': selected_order,
            'selected_test': selected_test,
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
                    results=add_order_form.cleaned_data['result'],
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

        # If form is invalid, re-render the page with errors
        view_order_form = viewLabOrders()
        view_test_form = viewLabTests()
        add_order_form = AddLabOrderForm()
        add_test_form = AddLabTestsForm()

        return render(request, 'labOrder.html', {
            'view_order_form': view_order_form,
            'add_order_form': add_order_form,
            'view_test_form': view_test_form,
            'add_test_form': add_test_form,
        })
