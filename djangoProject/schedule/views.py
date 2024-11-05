from django.shortcuts import render
from django.views import View
from sharedModels.models import Appointments, Employees
from .forms import PhysicianSelectionForm
from datetime import datetime, timedelta

class ScheduleView(View):
    def get(self, request):  # `request` is passed correctly here
        form = PhysicianSelectionForm()
        available_slots = {}
        current_date = datetime.now().date()

        # Initialize available slots for the next 7 days
        for i in range(30):  # Loop through the next 7 days
            day = current_date + timedelta(days=i)
            available_slots[day] = [
                {
                    'time': datetime.combine(day, datetime.min.time()).replace(hour=hour),
                    'is_booked': False
                }
                for hour in range(9, 17)
            ]

        # Check if a physician is selected
        selected_physician_id = request.GET.get('physician')
        if selected_physician_id:
            # Get all appointments for the selected physician
            appointments = Appointments.objects.filter(physcianid_id=selected_physician_id)

            # Remove booked slots from available slots
            booked_times = {(appt.date.date(), appt.date.hour) for appt in appointments}

            for day, slots in available_slots.items():
                for slot in slots:
                    if (day, slot['time'].hour) in booked_times:
                        slot['is_booked'] = True

        return render(request, 'SCHED.html', {'form': form, 'available_slots': available_slots})
