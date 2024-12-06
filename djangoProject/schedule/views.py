from django.shortcuts import render
from django.views import View
from sharedModels.models import Appointments, Employees, PatientRecord
from .forms import PhysicianSelectionForm, MakeAppointmentForm, viewPhysicianForm
from datetime import datetime, timedelta
from django.shortcuts import redirect

class ScheduleView(View):
    def getAppointments(self,physician):
        
        appointments = Appointments.objects.filter(physcianid=physician.employeeid)
        available_slots = {}
        earliest_apt = -1 #initilize so we can store the first
        current_date = datetime.now().date()

        #create empty time slots for next 60 days
        for i in range(60):
            day = current_date + timedelta(days=i)
            available_slots[day] = [
        {'time': datetime.combine(day, datetime.min.time()) + timedelta(hours=hour, minutes=minute),
            'is_booked': False
        }
        for hour in range(9, 17)  # Hours from 9 AM to 5 PM
        for minute in (0, 30)    # Half-hour increments (0 and 30 minutes past each hour)
    ]
        #list of appointment start and end times 
        apptIntervals= [{'start':(appt.date.date(),appt.date.time()), 'end':(appt.enddate.date(), appt.enddate.time())} for appt in appointments]
        
        # mark slots inbetween start and end times as booked 
        for day, slots in available_slots.items():
            for interval in apptIntervals:
                for slot in slots:

                    if(slot['time'].date() >= interval['start'][0]):
                        if(slot['time'].time() >= interval['start'][1]):
                            if(slot['time'].date() <= interval['end'][0]):
                                if(slot['time'].time() <= interval['end'][1]):
                                    slot['is_booked'] = True


                        # if(slot['time'].time < interval['end']):
                        #     slot['is_booked'] = True

                    
        return (available_slots)
                    
       
        
    def get(self, request):  # `request` is passed correctly here
        form = PhysicianSelectionForm()
        postForm = MakeAppointmentForm()
        available_slots = {}

        #if loaded with no info passed
        if( request.GET.get('physician') == None):
            return render(request, 'SCHED.html', {'form': form, 'postForm': postForm, 'available_slots': available_slots})
       
        #get request info
        physician_ID = request.GET.get('physician')
        physician = Employees.objects.get(employeeid = physician_ID)
        patient_ID = request.GET.get('patient')
        patient = PatientRecord.objects.get(patientid=patient_ID)
        
        available_slots= self.getAppointments(physician)
       
    
        #if time was chosen for calendar, pass that time
        if(request.GET.get('date') != None):
            startTime= datetime.strptime(request.GET.get('date').strip(), '%b. %d, %Y, %H:%M')
            endTime = datetime.strptime(request.GET.get('enddate').strip(), '%b. %d, %Y, %H:%M')
        else:
            return render(request, 'SCHED.html', {'form': form, 'available_slots': available_slots,'physician':physician, 'patient':patient})
    
            


        return render(request, 'SCHED.html', {'form': form, 'available_slots': available_slots, 'startTime': startTime, 'endTime': endTime,'physician':physician, 'patient':patient})
    
    def post(self,request):
          # Get data from the form (hidden inputs)
        startTime = request.POST.get('startTime')  # This is the time selected for the appointment
        print(startTime)
        endTime = request.POST.get('endTime')
        print(endTime)
        
        physician_id = request.POST.get('physicianid')  # Physician ID
        patient_id = request.POST.get('patientid')  # Patient ID

        startTime =datetime.strptime(startTime.strip(), '%b. %d, %Y, %H:%M')
        endTime = datetime.strptime(endTime.strip(), '%b. %d, %Y, %H:%M')
        physician = Employees.objects.get(employeeid=physician_id)
        patient = PatientRecord.objects.get(patientid =  patient_id )
        

        # try:
        #     physician = Employees.objects.get(employeeid=physician_id)
        #     patient = PatientRecord.objects.get(patientid=patient_id)
        # except Employees.DoesNotExist:
        #     # Handle the case where the physician doesn't exist
        #     return render(request, 'SCHED.html', {'error': 'Physician not found'})
        # except PatientRecord.DoesNotExist:
        #     # Handle the case where the patient doesn't exist
        #     return render(request, 'SCHED.html', {'error': 'Patient not found'})
        # parsed_datetime = datetime.strptime(selected_time.replace("a.m.", "AM").replace("p.m.", "PM").replace("noon","12:00 PM"), "%b. %d, %Y, %I:%M %p")
         # Create a new appointment
        appointment = Appointments.objects.create(
            date= startTime ,
            enddate = endTime,
            physcianid= physician,
            patientid= patient
        )
        
        return redirect(f"/schedule/?physician={physician_id}&patient={patient_id}")
class findPhysicianView(View):
    def get(self, request):
       if(request.GET.get('physician') == None):
        return render(request, 'findPhysician.html', {'select':viewPhysicianForm})
       
       physicianID = request.GET.get('physician')
       physicianObject = Employees.objects.get(employeeid = physicianID)

       return render(request, 'findPhysician.html', {'select':viewPhysicianForm, 'physician':physicianObject})
    




