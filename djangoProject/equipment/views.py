from django.shortcuts import render
from django.views import View
from sharedModels.models import Equipment
from django.shortcuts import redirect

class EquipmentView(View):
    def get(self, request):
        # Retrieve the search query from the GET request
        query = request.GET.get('equipmentid', '')  # Default to empty string if not found
        
        if query:
            # Filter Equipment objects based on the equipmentid if query exists
            items = Equipment.objects.filter(equipmentid=query)
        else:
            # Retrieve all items if no query is provided
            items = Equipment.objects.all()
        
        # Render the template and pass the filtered items and query
        return render(request, 'equipment.html', {'items': items, 'query': query})

    def post(self, request):
        # Handle the POST request for adding equipment (same as before)
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

        # Redirect to the same page after adding equipment to avoid duplicate submissions
        return redirect('equipment')
