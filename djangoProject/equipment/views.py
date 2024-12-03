from django.shortcuts import render
from django.views import View
from sharedModels.models import Equipment, Maintenance
from django.shortcuts import redirect

class ManageView(View):
    def get(self, request):
        return render(request, 'manage_page.html')
    
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

        #In case it already exists, be nice and tell them no can do
        if Equipment.objects.filter(equipmentid=equipmentid).exists():
            return render(request, 'equipment.html', {
                'error': f'Equipment ID {equipmentid} already exists.',
                'query': request.GET.get('equipmentid', ''),
                'query_type': request.GET.get('type', '')
        })
        # Create and save a new Equipment object
        Equipment.objects.create(
            equipmentid=equipmentid,
            type=type,
            description=description,
            lease_terms=lease_terms,
            departmentleased=departmentleased,
            owned_lease=owned_lease,
            purchasedate=purchasedate,
            warenty_info=warenty_info,
        )
        # Redirect to the same page after adding equipment
        return render('manage_page.html')

class ProblemsView(View):
    def get(self, request):
        # Get all open problems (status not 'resolved' or other criteria for open)
        open_problems = Maintenance.objects.filter(status='Open')  # Or use other criteria for open problems
        
        # Pass the open problems and their corresponding equipment to the template
        return render(request, 'problems_page.html', {'open_problems': open_problems})

    def post(self, request):
        # Get the data from the form
        equipmentid = request.POST.get('equipmentid')
        type = request.POST.get('type')
        description = request.POST.get('description', '')
        status = request.POST.get('status')
        resolution = request.POST.get('resolution', '')

        # Check if the equipment exists, store the instance
        equipment = Equipment.objects.filter(equipmentid=equipmentid).first()
        if equipment:
            # Create a new maintenance problem entry
            Maintenance.objects.create(
            equipmentid=equipment,
            type=type,
            description=description,
            status=status,
            resolution=resolution,
            )
            return render(request, 'problems_page.html', {'success': 'Problem added successfully.'})
        else:
            return render(request, 'problems_page.html', {'error': 'Equipment not found.'})

        # Redirect to a page that shows the equipment or maintenance list

#Currently not used
class AddProblemView(View):
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


class EquipmentView(View):

    def get(self, request):
        # Retrieve the search query from the GET request
        inventory_query = request.GET.get('equipmentid', '')  # Default to empty string if not found
        type_query = request.GET.get('type', '')

        filters = {}
        if inventory_query:
            filters['equipmentid'] = inventory_query
        if type_query:
            filters['type__icontains'] = type_query #icontains = case insensitive

        for f in filters:
            print(f"Filters: {f}")
        #Based on filter, fetch equipment
        items = Equipment.objects.filter(**filters)

        #Check if results found
        if items.exists():
            #Now there can be multiple results, this stores them
            results = []
            for item in items:
                # Determine additional details based on 'Owned/Lease' flag for each model
                if item.owned_lease == 'O':  # 'O' for Owned
                    extra_info = {
                        'purchasedate': item.purchasedate,
                        'warenty_info': item.warenty_info
                    }
                elif item.owned_lease == 'L':  # 'L' for Leased
                    extra_info = {
                        'lease_terms': item.lease_terms
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
                #Store results for each object in queryset
                results.append(details)
            context = {'results': results, 'query_id': inventory_query, 'query_type': type_query}
        else:
            #Show error message
            context = {'error': 'No equipment found matching the criteria.', 'query_id': inventory_query, 'query_type': type_query}

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

        #In case it already exists, be nice and tell them no can do
        if Equipment.objects.filter(equipmentid=equipmentid).exists():
            return render(request, 'equipment.html', {
                'error': f'Equipment ID {equipmentid} already exists.',
                'query': request.GET.get('equipmentid', ''),
                'query_type': request.GET.get('type', '')
        })
        # Create and save a new Equipment object
        Equipment.objects.create(
            equipmentid=equipmentid,
            type=type,
            description=description,
            lease_terms=lease_terms,
            departmentleased=departmentleased,
            owned_lease=owned_lease,
            purchasedate=purchasedate,
            warenty_info=warenty_info,
        )

        # Redirect to the same page after adding equipment
        return redirect('equipment')


#class EquipmentManage(View):
