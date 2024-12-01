from django.shortcuts import render
from django.views import View
from sharedModels.models import Equipment
from django.shortcuts import redirect

def manage_page(request):
    return render(request, 'manage_page.html')

class EquipmentView(View):

    def get(self, request):
        # Retrieve the search query from the GET request
        inventory_query = request.GET.get('equipmentid', '')  # Default to empty string if not found

        if inventory_query:
            try:
                # Fetch a specific equipment object by equipmentid
                item = Equipment.objects.get(equipmentid=inventory_query)

                # Determine additional details based on 'Owned/Lease' flag
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

                context = {'details': details, 'query': inventory_query}
            except Equipment.DoesNotExist:
                # If equipment with the given ID does not exist, show an error
                context = {'error': 'No equipment found with the provided ID.', 'query': query}
        else:
            # Show all equipment if no specific query is provided
            items = Equipment.objects.all()
            context = {'items': items, 'query': inventory_query}

        # Render the template and pass the context
        return render(request, 'equipment.html', context)

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
