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
        for i in range(60):
            day = current_date + timedelta(days=i)
            available_slots[day] = [
        {
            'time': datetime.combine(day, datetime.min.time()) + timedelta(hours=hour, minutes=minute),
            'is_booked': False
        }
        for hour in range(9, 17)  # Hours from 9 AM to 5 PM
        for minute in (0, 30)    # Half-hour increments (0 and 30 minutes past each hour)
    ]
        # Remove booked slots from available slots
        apptEnds = {appt.date for appt in Appointments.objects.all()}
        apptStarts = {appt.enddate for appt in Appointments.objects.all()}
        apptIntervals = (apptStarts,apptEnds)

        # print(apptEnds)
        # print(apptStarts)
        # bookedTimes=[]
        # for (start,end) in appointmentIntervals:
            
        #     currentTime = start
        #     while currentTime < end:

        #         justDate= currentTime.date()
        #         print(type(justDate))
        #         bookedTimes.append((justDate,currentTime.hour,currentTime.minute))
        #         currentTime = currentTime + timedelta(minutes=30)
        
        # for day,slots in available_slots.items():
        #     for slot in slots:
        #         if(day, slot['time'].hour,slot['time'].minute) in 
                    

        # booked_times = {(appt.date.date(), appt.date.hour, appt.date.minute) for appt in appointments}
        for day, slots in available_slots.items():
                for slot in slots:
                    print(type(slot['time']))
                    print(type(apptStarts[1]))
                    # if (day, slot['time'].hour, slot['time'].minute) in bookedTimes:
                    #     slot['is_booked'] = True
                    # elif(earliest_apt == -1):
                    #     earliest_apt= slot['time']
        return (available_slots, earliest_apt)
                    
       
        
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
        
        available_slots, selected_time = self.getAppointments(physician)
       
    
            #if time was chosen for calendar, pass that time, else, select earliest appointment
        if(request.GET.get('date') != None):
            startTime= datetime.strptime(request.GET.get('date').strip(), '%b. %d, %Y, %H:%M')
            endTime = datetime.strptime(request.GET.get('enddate').strip(), '%b. %d, %Y, %H:%M')
        else:
            startTime= selected_time
            return render(request, 'SCHED.html', {'form': form, 'available_slots': available_slots,'physician':physician, 'patient':patient})
    
            


        return render(request, 'SCHED.html', {'form': form, 'available_slots': available_slots, 'startTime': startTime, 'endTime': endTime,'physician':physician, 'patient':patient})
    
    def post(self,request):
          # Get data from the form (hidden inputs)
        startTime = request.POST.get('startTime')  # This is the time selected for the appointment
        endTime = request.POST.get('endTime')
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
    




