from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from sharedModels.models import Appointments, Employees, PatientRecord
from .forms import PhysicianSelectionForm, AppointmentForm, viewPhysicianForm
from datetime import datetime, timedelta, timezone

class ScheduleView(View):
    def getAppointments(self, physician):
        
        appointments = Appointments.objects.filter(physcianid=physician.employeeid)
        available_slots = {}
        earliest_apt = -1  # initialize so we can store the first
        current_date = datetime.now().date()

        # create empty time slots for next 60 days
        for i in range(60):
            day = current_date + timedelta(days=i)
            available_slots[day] = [
                {'time': datetime.combine(day, datetime.min.time(), tzinfo=timezone.utc) + timedelta(hours=hour, minutes=minute),
                 'is_booked': False,
                 'appt': None
                 }
                for hour in range(9, 17)  # Hours from 9 AM to 5 PM
                for minute in (0, 30)  # Half-hour increments (0 and 30 minutes past each hour)
            ]
        # list of appointment start and end times
        # apptIntervals= [{'start':(appt.date.date(),appt.date.time()), 'end':(appt.enddate.date(), appt.enddate.time()), 'appt': appt} for appt in appointments]
        apptIntervals = [{'start': appt.date, 'end': appt.enddate, 'appt': appt} for appt in appointments]
        # mark slots in between start and end times as booked
        for day, slots in available_slots.items():
            for interval in apptIntervals:
                for slot in slots:
                    if (slot['time'] >= interval['start']):
                        if (slot['time'] < interval['end']):
                            slot['is_booked'] = True
                            slot['appt'] = interval['appt']

        return (available_slots)

    def get(self, request):  # `request` is passed correctly here

        form = PhysicianSelectionForm()

        available_slots = {}

        # if loaded with no info passed
        if (request.GET.get('physician') == None):
            return render(request, 'SCHED.html', {'form': form, 'available_slots': available_slots})

        # get request info
        physician_ID = request.GET.get('physician')
        physician = Employees.objects.get(employeeid=physician_ID)
        form.fields['physician'].initial = physician_ID  
        # set Appointment form with physician and patient info 
        appointment_Form = AppointmentForm()
        appointment_Form.fields['physcianid'].initial = physician_ID

        available_slots = self.getAppointments(physician)

        # if time was chosen for calendar, pass that time
        if (request.GET.get('date') != None):
            startTime = datetime.strptime(request.GET.get('date').strip(), '%b. %d, %Y, %H:%M')
            endTime = datetime.strptime(request.GET.get('enddate').strip(), '%b. %d, %Y, %H:%M')
            print(startTime)
        else:
            return render(request, 'SCHED.html', {'form': form, 'available_slots': available_slots, 'physician': physician})
        # get request info
        # get request info

        appointment_Form.fields['date'].initial = startTime
        appointment_Form.fields['enddate'].initial = endTime
        print(type(appointment_Form.fields['date'].initial))

        print(appointment_Form.fields['physcianid'].initial)
        return render(request, 'SCHED.html', {'form': form, 'available_slots': available_slots, 'appointment_form': appointment_Form, 'physician': physician})

    def post(self, request):
        # Get data from the form (hidden inputs)
        date_string = request.POST.get('date')
        enddate_string = request.POST.get('enddate')
        physician_id = request.POST.get('physician')
        patient_id = request.POST.get('patientid')
        aptType = request.POST.get('aptType')
        description = request.POST.get('description')

        # Convert date strings to datetime objects

        startTime = datetime.strptime(request.POST.get('date').strip(), '%b. %d, %Y, %H:%M')
        endTime = datetime.strptime(request.POST.get('enddate').strip(), '%b. %d, %Y, %H:%M')

        # Retrieve physician and patient objects
        physician = Employees.objects.get(employeeid=physician_id)
        if (patient_id):
            patient = PatientRecord.objects.get(patientid=patient_id)

        # Create a new appointment
        if (patient_id):
            appointment = Appointments.objects.create(
                date=startTime,
                enddate=endTime,
                physcianid=physician,
                patientid=patient,
                aptType=aptType,
                description=description
            )
        else:
            appointment = Appointments.objects.create(
                date=startTime,
                enddate=endTime,
                physcianid=physician,
                aptType=aptType,
                description=description
            )

        return redirect(f"/schedule/?physician={physician_id}&patient={patient_id}")

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
        # appointment = Appointments.objects.create(
        #     date= startTime ,
        #     enddate = endTime,
        #     physcianid= physician,
        #     patientid= patient
        # )

        return redirect(f"/schedule/?physician={physician_id}&patient={patient_id}")


class findPhysicianView(View):
    def get(self, request):
        if (request.GET.get('physician') == None):
            return render(request, 'findPhysician.html', {'select': viewPhysicianForm})

        physicianID = request.GET.get('physician')
        physicianObject = Employees.objects.get(employeeid=physicianID)

        return render(request, 'findPhysician.html', {'select': viewPhysicianForm, 'physician': physicianObject})





def cancel_appointment(request, appt_id):
    appointment = Appointments.objects.get(appointmentid=appt_id)
    if request.method == 'POST':
        appointment.delete()
        referer = request.META.get('HTTP_REFERER')
        return redirect(referer)  # Redirect to the schedule page after deletion


