from django.shortcuts import render
from django.views import View
from sharedModels.models import Appointments, Employees, PatientRecord
from .forms import PhysicianSelectionForm, MakeAppointmentForm
from datetime import datetime, timedelta

class ScheduleView(View):
    def get(self, request):  # `request` is passed correctly here
        form = PhysicianSelectionForm()
        postForm = MakeAppointmentForm()
        available_slots = {}

        #if loaded with no info passed
        if( request.GET.get('physician') == None):
            return render(request, 'SCHED.html', {'form': form, 'postForm': postForm, 'available_slots': available_slots})
       
    
        current_date = datetime.now().date()
        #set to -1 so we know no info has been passed
        selected_time =-1
        
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
        physician = Employees.objects.get(employeeid=selected_physician_id)

        #get patient
        selected_patient_id = request.GET.get('patient')
        patient = PatientRecord.objects.get(patientid= selected_patient_id)
        if selected_physician_id:
            # Get all appointments for the selected physician
            appointments = Appointments.objects.filter(physcianid_id=selected_physician_id)

            # Remove booked slots from available slots
            booked_times = {(appt.date.date(), appt.date.hour) for appt in appointments}

            for day, slots in available_slots.items():
                for slot in slots:
                    if (day, slot['time'].hour) in booked_times:
                        slot['is_booked'] = True
                    elif(selected_time == -1): 
                        selected_time = slot['time'].strftime("%b %d, %Y, %I:%M %p")
                    if(request.GET.get('changed_time') != None):
                        selected_time = request.GET.get('changed_time')


        return render(request, 'SCHED.html', {'form': form, 'available_slots': available_slots, 'selected_time': selected_time,'physician':physician, 'patient':patient})

    def post(self,request):
          # Get data from the form (hidden inputs)
        selected_time = request.POST.get('date')  # This is the time selected for the appointment
        physician_id = request.POST.get('physicianid')  # Physician ID
        patient_id = request.POST.get('patientid')  # Patient ID

        try:
            physician = Employees.objects.get(employeeid=physician_id)
            patient = PatientRecord.objects.get(patientid=patient_id)
        except Employees.DoesNotExist:
            # Handle the case where the physician doesn't exist
            return render(request, 'SCHED.html', {'error': 'Physician not found'})
        except PatientRecord.DoesNotExist:
            # Handle the case where the patient doesn't exist
            return render(request, 'SCHED.html', {'error': 'Patient not found'})
        selected_time = selected_time.replace('.', ',') 
        parsed_datetime = datetime.strptime(selected_time, "%b %d, %Y, %I:%M %p")
        formatted_datetime = parsed_datetime.strftime("%Y-%m-%d %H:%M:%S")
         # Create a new appointment
        appointment = Appointments.objects.create(
            date= formatted_datetime,
            physcianid=physician,
            patientid= patient
        )
        form = PhysicianSelectionForm()
        postForm = MakeAppointmentForm()
        available_slots = {}
        return render(request, 'SCHED.html', {'form': form, 'postForm': postForm, 'available_slots': available_slots,'physician':physician_id, 'patient':patient_id})
       