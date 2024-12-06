from django.shortcuts import render
from django.views import View
from equipment.models import Equipment, Maintenance, Vendor
from django.shortcuts import redirect, get_object_or_404
from django.db.models import Count, Avg, F, ExpressionWrapper, DurationField

class ManageView(View):
    def get(self, request):

        #Get all the available vendors the user can choose when creating
        #A new equipment table
        vendors = Vendor.objects.all()
        return render(request, 'manage_page.html', {'vendors': vendors})
    
    def post(self, request):
        # Handle the POST request for adding equipment
        equipmentid = request.POST.get('equipmentid')
        type = request.POST.get('type')
        description = request.POST.get('description', '')
        lease_terms = request.POST.get('lease_terms', '')
        departmentleased = request.POST.get('departmentleased', '')
        owned_lease = request.POST.get('owned_lease')
        purchasedate = request.POST.get('purchasedate', None) #None values can be empty and not cause problems
        warenty_info = request.POST.get('warenty_info', '')
        lease_start = request.POST.get('lease_start', None)
        lease_end = request.POST.get('lease_end', None)
        vendor_id = request.POST.get('vendor', '')

        #In case it already exists, be nice and tell them no can do
        if Equipment.objects.filter(equipmentid=equipmentid).exists():
            vendors = Vendor.objects.all() # After form submissions, vendor is repopulated
            return render(request, 'manage_page.html', {
                'error': f'Equipment ID {equipmentid} already exists.',
                'vendors': vendors,  # Include vendors for the dropdown
        })

        #If provided, get vendor
        vendor = Vendor.objects.filter(vendorid=vendor_id).first() if vendor_id else None

        # Only occurs if equipment is being leased
        if owned_lease == 'L':  # Leased equipment
            if not lease_start or not lease_end:
                vendors = Vendor.objects.all()
                return render(request, 'manage_page.html', {
                    'error': 'Both lease start and end dates are required for leased equipment.',
                    'vendors': vendors,
                })
        # Create and save a new Equipment object
        equipment = Equipment.objects.create(
            equipmentid=equipmentid,
            type=type,
            description=description,
            lease_terms=lease_terms,
            departmentleased=departmentleased,
            owned_lease=owned_lease,
            purchasedate=purchasedate if owned_lease == 'O' else None,
            warenty_info=warenty_info if owned_lease == 'O' else '',
            lease_start=lease_start if owned_lease == 'L' else None,
            lease_end=lease_end if owned_lease == 'L' else None,
            vendor=vendor,
        )

        if vendor:
            equipment.vendor = vendor
            equipment.save() # Save with vendor association if required
        # Redirect to the same page after adding equipment
        vendors = Vendor.objects.all() # Repopulate vendor dropdown
        return render(request, 'manage_page.html', {
            'success': f'Equipment {equipmentid} successfully added.',
            'vendors': vendors,  # Include vendors for the dropdown
        })

class ProblemsView(View):
    def get(self, request):
        # Get the status from the request; default to 'Open'
        status = request.GET.get('status', 'Open')
        
        # Filter problems based on the status
        problems = Maintenance.objects.filter(status=status)
        
        # Pass the problems and the current status to the template
        return render(request, 'problems_page.html', {
            'problems': problems,
            'current_status': status,
        })

    def post(self, request):
        # Handle problem creation
        equipmentid = request.POST.get('equipmentid')
        problem_type = request.POST.get('problemtype')  # Correct field name
        description = request.POST.get('description', '')
        status = request.POST.get('status')
        resolution = request.POST.get('resolution', '')

        # Check if the equipment exists, store the instance
        equipment = Equipment.objects.filter(equipmentid=equipmentid).first()
        if equipment:
            # Create a new maintenance problem entry
            Maintenance.objects.create(
                equipmentid=equipment,
                type=problem_type,  # Correct variable name
                description=description,
                status=status,
                resolution=resolution,
            )
            return render(request, 'problems_page.html', {'success': 'Problem added successfully.'})
        else:
            return render(request, 'problems_page.html', {'error': 'Equipment not found.'})


class CloseProblemsView(View):
    template_name = 'close_problem.html'

    def get(self, request):
        # Render the close problem form
        return render(request, self.template_name)

    def post(self, request):
        # Handle form submission
        maintenanceid = request.POST.get('maintenanceid')
        resolution = request.POST.get('resolution')

        try:
            # Fetch the existing maintenance record
            maintenance = get_object_or_404(Maintenance, maintenanceid=maintenanceid)
            # Update the record
            maintenance.status = "Closed"
            maintenance.resolution = resolution
            maintenance.save()

        except Exception as e:
            return render(request, 'problems_page.html', f"Error closing Problem: {e}")

        return render(request,'problems_page.html',{'success': 'Problem closed successfully.'}) 

class StatisticalReportView(View):
    template_name = 'statistics_report.html'

    def get(self, request):
        # Retrieve the start and end date from GET parameters
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        # Filter maintenance records within the specified period
        maintenance_records = Maintenance.objects.filter(
            created_at__range=[start_date, end_date]
        ) if start_date and end_date else Maintenance.objects.all()

        # Annotate average time to close by calculating the duration between created_at and resolution
        maintenance_data = maintenance_records.annotate(
            time_to_close=ExpressionWrapper(
                F('resolution') - F('created_at'),
                output_field=DurationField()
            )
        )

        # Group by problem type and vendor with statistics
        summary_by_type_and_vendor = maintenance_data.values(
            'type', 'equipmentid__vendor__name'
        ).annotate(
            total_problems=Count('maintenanceid'),
            avg_time_to_close=Avg('time_to_close')
        ).order_by('type', 'equipmentid__vendor__name')

        # Pass the data to the template
        return render(request, self.template_name, {
            'summary_by_type_and_vendor': summary_by_type_and_vendor,
            'start_date': start_date,
            'end_date': end_date,
        })

#Currently not used
class AddProblemType(View):
    def post(self, request):
        # Add a new problem type
        new_problem_type = request.POST.get('type', '').strip()
        if new_problem_type:
            # Check if the problem type already exists
            if not Maintenance.objects.filter(name=new_problem_type).exists():
                Maintenance.objects.create(name=new_problem_type)
                return redirect('problems_page')
            else:
                return render(request, 'problems_page.html', {
                    'error': 'Problem type already exists.',
                })
        else:
            return render(request, 'problems_page.html', {
                'error': 'Problem type cannot be empty.',
            })

class VendorView(View):
    def get(self, request):
        # Retrieve search queries from the GET request
        vendorid_query = request.GET.get('vendorid', '')
        name_query = request.GET.get('name', '')
        equipment_type_query = request.GET.get('equipment_type', '')  # New query parameter

        filters = {}
        if vendorid_query:
            filters['vendorid__icontains'] = vendorid_query
        if name_query:
            filters['name__icontains'] = name_query
        if equipment_type_query:
            filters['equipment_types__icontains'] = equipment_type_query  # Assuming equipment_types is a field on Vendor

        for f in filters:
            print(f"Filters: {f}")

        # Based on the filters, fetch vendors
        vendors = Vendor.objects.filter(**filters)

        if vendors.exists():
            vendor_results = []
            for vendor in vendors:
                vendor_details = {
                    'name': vendor.name,
                    'vendorid': vendor.vendorid,
                    'address': vendor.address,
                    'equipment_types': vendor.equipment_types,
                    'preferred': vendor.preferred,
                }
                vendor_results.append(vendor_details)

            context = {
                'vendor_results': vendor_results,
                'query_vendorid': vendorid_query,
                'query_name': name_query,
                'query_equipment_type': equipment_type_query,  # Pass the equipment_type to the template
            }
        else:
            context = {
                'error': 'No vendors found matching the criteria.',
                'query_vendorid': vendorid_query,
                'query_name': name_query,
                'query_equipment_type': equipment_type_query,
            }
        return render(request, 'equipment.html', context)
    
    def post(self, request):
        # Extract data from the form
        vendorid = request.POST.get('vendorid')
        name = request.POST.get('name')
        address = request.POST.get('address')
        equipment_types = request.POST.get('equipment_types')
        preferred = request.POST.get('preferred') == 'on'  # Check if checkbox is checked

        # Check if a vendor with the same name already exists
        if Vendor.objects.filter(name=name).exists():
            return render(request, 'vendor_add.html', {'error': 'Vendor with this name already exists.'})

        # Create and save the vendor object
        Vendor.objects.create(
            vendorid=vendorid,
            name=name,
            address=address,
            equipment_types=equipment_types,
            preferred=preferred
        )
        print(f"VendorID: {vendorid}, Name: {name}, Address: {address}")

        # Redirect to a success page or back to the vendor list
        return redirect('manage_page')  # Assuming you have a list view for vendors

class EquipmentView(View):
    def get(self, request):
        # Retrieve the search query from the GET request
        inventory_query = request.GET.get('equipmentid', '')  # Default to empty string if not found
        type_query = request.GET.get('type', '')

        filters = {}
        if inventory_query:
            filters['equipmentid'] = inventory_query
        if type_query:
            filters['type__icontains'] = type_query  # case-insensitive search

        equipment_results = []  # Default to an empty list in case no results are found

        if inventory_query or type_query:  # Only search if either query is present
            for f in filters:
                print(f"Filters: {f}")
            # Fetch equipment based on the filters
            items = Equipment.objects.filter(**filters)

            if items.exists():
                for item in items:
                    # Determine additional details based on 'Owned/Lease' flag for each model
                    if item.owned_lease == 'O':  # 'O' for Owned
                        extra_info = {
                            'purchasedate': item.purchasedate,
                            'warenty_info': item.warenty_info
                        }
                    elif item.owned_lease == 'L':  # 'L' for Leased
                        extra_info = {
                            'vendor': item.vendor,
                            'lease_terms': item.lease_terms,
                            'lease_start': item.lease_start,
                            'lease_end': item.lease_end
                        }
                    else:
                        extra_info = {}
                    # Combine main and extra details
                    details = {
                        'equipmentid': item.equipmentid,
                        'type': item.type,
                        'description': item.description,
                        'departmentleased': item.departmentleased,
                        'owned_lease': item.owned_lease,
                        **extra_info
                    }
                    equipment_results.append(details)

            if not equipment_results:
                # If no equipment found, set an error message
                context = {'error': 'No equipment found matching your search criteria.',
                           'query_id': inventory_query, 'query_type': type_query}
            else:
                context = {'equipment_results': equipment_results, 'query_id': inventory_query, 'query_type': type_query}
        else:
            # Show an empty page or message if no search query is provided
            context = {'query_id': inventory_query, 'query_type': type_query}

        # Render the template and pass the context
        return render(request, 'equipment.html', context)


    #Post method below is done in manage_html, just scared to delete it
    def post(self, request):
        # Handle the POST request for adding equipment
        equipmentid = request.POST.get('equipmentid')
        type = request.POST.get('type')
        description = request.POST.get('description', '')
        lease_terms = request.POST.get('lease_terms', '')
        departmentleased = request.POST.get('departmentleased', '')
        owned_lease = request.POST.get('owned_lease')
        purchasedate = request.POST.get('purchasedate', None)
        warenty_info = request.POST.get('warenty_info', '')
        vendor_id = request.POST.get('vendor')

        #In case it already exists, be nice and tell them no can do
        if Equipment.objects.filter(equipmentid=equipmentid).exists():
            return render(request, 'equipment.html', {
                'error': f'Equipment ID {equipmentid} already exists.',
                'query': request.GET.get('equipmentid', ''),
                'query_type': request.GET.get('type', '')
        })

        vendor = Vendor.objects.filter(id=vendor_id).first() if vendor_id else None

        # Create and save a new Equipment object
        equipment = Equipment.objects.create(
            equipmentid=equipmentid,
            type=type,
            description=description,
            lease_terms=lease_terms,
            departmentleased=departmentleased,
            owned_lease=owned_lease,
            purchasedate=purchasedate,
            warenty_info=warenty_info,
        )

        if vendor:
            equipment.vendor = vendor
            equipment.save()  # Save with vendor association if required

        # Redirect to the same page after adding equipment
        return redirect('equipment')

class DepartmentView(View):
    def get(self, request):
        # Retrieve department query from the GET request
        department_query = request.GET.get('departmentleased', '')

        # Filter equipment by department if provided
        if department_query:
            equipment_list = Equipment.objects.filter(departmentleased__icontains=department_query)
        else:
            equipment_list = Equipment.objects.all()

        # Group equipment by departmentleased
        grouped_equipment = {}
        for item in equipment_list:
            department = item.departmentleased
            if department not in grouped_equipment:
                grouped_equipment[department] = []
            grouped_equipment[department].append(item)

        # Pass the grouped equipment list and query back to the template
        context = {
            'grouped_equipment': grouped_equipment,
            'department_query': department_query,
        }

        return render(request, 'equipment.html', context)