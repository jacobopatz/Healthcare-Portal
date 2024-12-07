# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from django.utils.timezone import now 
import uuid


class Appointments(models.Model):
    ROUTINE = 'routine'
    URGENT_CARE = 'urgent_care'
    FOLLOW_UP = 'follow_up_visit'
    NA = 'N/A'
    APT_TYPE_CHOICES = [
        (ROUTINE, 'Routine'),
        (URGENT_CARE, 'Urgent Care'),
        (FOLLOW_UP, 'Follow-Up Visit'),
        (NA,'N/A')
    ]
    appointmentid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Field name made lowercase.
    date = models.DateTimeField(db_column='Date')
    enddate = models.DateTimeField(db_column='enddate', null=True)
    physcianid = models.ForeignKey('Employees', models.DO_NOTHING, db_column='PhyscianID')  # Field name made lowercase.
    patientid = models.ForeignKey('PatientRecord', models.DO_NOTHING,
                                  db_column='PatientID')  # Field name made lowercase.
    
    aptType = aptType = models.CharField(
        max_length=20,
        choices=APT_TYPE_CHOICES,
        default=NA,  # You can set the default to one of the choices
    )

    class Meta:
        db_table = 'appointments'

    def __str__(self):
        return f"(ID: {self.appointmentid} start: {self.date} end: {self.enddate} physician: {self.physcianid} patient: {self.patientid})"


class Employees(models.Model):
    employeeid = models.AutoField(db_column='EmployeeID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=45)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=45)  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=20)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=15)  # Field name made lowercase.
    workdays = models.CharField(db_column='WorkDays', max_length=20)  # Field name made lowercase.

    class Meta:
        db_table = 'employees'

    def __str__(self):
        return f"(ID: {self.employeeid}) {self.firstname} {self.lastname}"  # Display first and last name


class Encounters(models.Model):
    encounterid = models.AutoField(db_column='EncounterID', default=0, primary_key=True)
    date = models.DateTimeField(db_column='Date')  # Field name made lowercase. The composite primary key (Date, PhysicianID) found, that is not supported. The first column is selected.
    physicianid = models.ForeignKey(Employees, models.DO_NOTHING, db_column='PhysicianID')  # Field name made lowercase.
    patientid = models.ForeignKey('PatientRecord', models.DO_NOTHING, db_column='PatientID')  # Field name made lowercase.
    patientcomplaints = models.CharField(db_column='PatientComplaints', max_length=120, blank=True, null=True)  # Field name made lowercase.
    vitalsigns = models.CharField(db_column='VitalSigns', max_length=120, blank=True, null=True)  # Field name made lowercase.
    practitionernotes = models.CharField(db_column='PractitionerNotes', max_length=120, blank=True, null=True)  # Field name made lowercase.
    laborderid = models.ForeignKey('LabOrders', models.DO_NOTHING, db_column='LabOrderID', null=True)  # Field name made lowercase.
    pharmacyorderid = models.ForeignKey('PharmacyOrder', models.DO_NOTHING, db_column='PharmacyOrderID', null=True)  # Field name made lowercase.
    treatment_plan = models.CharField(db_column='Treatment Plan', max_length=120, blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    refferals = models.CharField(db_column='Refferals', max_length=120, blank=True, null=True)  # Field name made lowercase.
    recfollowup = models.DateField(db_column='RecFollowUp', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'encounters'
        unique_together = (('date', 'physicianid'),)


class Equipment(models.Model):
    equipmentid = models.IntegerField(db_column='EquipmentID', primary_key=True)  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=45)  # Field name made lowercase.
    lease_terms = models.CharField(db_column='Lease Terms', max_length=45, blank=True,
                                   null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    description = models.CharField(db_column='Description', max_length=120, blank=True,
                                   null=True)  # Field name made lowercase.
    departmentleased = models.CharField(db_column='DepartmentLeased', max_length=45, blank=True,
                                        null=True)  # Field name made lowercase.
    owned_lease = models.CharField(db_column='Owned/Lease',
                                   max_length=1)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    purchasedate = models.DateField(db_column='PurchaseDate', blank=True, null=True)  # Field name made lowercase.
    warenty_info = models.CharField(db_column='Warenty Info', max_length=120, blank=True,
                                    null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.

    class Meta:
        db_table = 'equipment'


class Insurance(models.Model):
    carrierid = models.AutoField(db_column='CarrierID', primary_key=True)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=20)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=45)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=120)  # Field name made lowercase.

    class Meta:
        db_table = 'insurance'


class Invoice(models.Model):
    lineitemid = models.AutoField(db_column='LineItemID', primary_key=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=120)  # Field name made lowercase.

    class Meta:
        db_table = 'invoice'


class LabOrders(models.Model):
    orderid = models.AutoField(db_column='OrderID', primary_key=True)  # Field name made lowercase.
    patientid = models.ForeignKey('PatientRecord', models.DO_NOTHING,
                                  db_column='PatientID')  # Field name made lowercase.
    physicianid = models.ForeignKey(Employees, models.DO_NOTHING, db_column='PhysicianID')  # Field name made lowercase.
    teststypeid = models.ForeignKey('LabTests', models.DO_NOTHING,
                                    db_column='TestsTypeID')  # Field name made lowercase.
    technicianid = models.ForeignKey(Employees, models.DO_NOTHING, db_column='TechnicianID',
                                     related_name='laborders_technicianid_set')  # Field name made lowercase.
    results = models.IntegerField(db_column='Results')  # Field name made lowercase.
    dateperfomed = models.DateTimeField(db_column='Dateperfomed', null=True)
    dateordered = models.DateTimeField(db_column='Dateordered', null=True)

    class Meta:
        db_table = 'lab orders'

    def __str__(self):
        return f"(ID: {self.orderid}) {self.patientid} {self.teststypeid} {self.results}"


class LabTests(models.Model):
    typeid = models.AutoField(db_column='TypeID', primary_key=True)  # Field name made lowercase.
    typename = models.CharField(db_column='TypeName', max_length=20)  # Field name made lowercase.
    normalrange = models.CharField(db_column='NormalRange', max_length=10)  # Field name made lowercase.
    urgentrange = models.CharField(db_column='UrgentRange', max_length=10)  # Field name made lowercase.

    class Meta:
        db_table = 'lab tests'
        db_table_comment = '\\n\\n\\n'

    def __str__(self):
        return f"(ID: {self.typeid}) {self.typename}"


class Maintenance(models.Model):
    maintenanceid = models.IntegerField(db_column='MaintenanceID',
                                        primary_key=True)  # Field name made lowercase. The composite primary key (MaintenanceID, EquipmentID) found, that is not supported. The first column is selected.
    equipmentid = models.ForeignKey(Equipment, models.DO_NOTHING, db_column='EquipmentID')  # Field name made lowercase.
    type = models.CharField(db_column='Type', max_length=45)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=120, blank=True,
                                   null=True)  # Field name made lowercase.
    status = models.CharField(db_column='Status', max_length=45)  # Field name made lowercase.
    resolution = models.CharField(db_column='Resolution', max_length=120, blank=True,
                                  null=True)  # Field name made lowercase.
    created_at = models.DateTimeField(default=now, db_column='CreatedAt')

    class Meta:
        db_table = 'maintenance'
        unique_together = (('maintenanceid', 'equipmentid'),)


class Medication(models.Model):
    medicationid = models.IntegerField(db_column='MedicationID', primary_key=True)  # Field name made lowercase.
    medicationname = models.CharField(db_column='MedicationName', max_length=20)  # Field name made lowercase.
    description = models.CharField(db_column='Description', max_length=120, blank=True,
                                   null=True)  # Field name made lowercase.
    recdosage = models.CharField(db_column='RecDosage', max_length=120)  # Field name made lowercase.
    recfreq = models.CharField(db_column='RecFreq', max_length=120)  # Field name made lowercase.
    sideeffects = models.CharField(db_column='SideEffects', max_length=120)  # Field name made lowercase.
    adversedrugs = models.CharField(db_column='AdverseDrugs', max_length=120)  # Field name made lowercase.

    class Meta:
        db_table = 'medication'


class PatientRecord(models.Model):
    patientid = models.AutoField(db_column='PatientID', primary_key=True)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=20)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=20)  # Field name made lowercase.
    phonenumber = models.CharField(db_column='PhoneNumber', max_length=15)  # Field name made lowercase.
    address = models.CharField(db_column='Address', max_length=45)  # Field name made lowercase.
    insuranceid = models.ForeignKey(Insurance, models.DO_NOTHING, db_column='InsuranceID')  # Field name made lowercase.
    dob = models.DateField(db_column='DOB')  # Field name made lowercase.
    gender = models.CharField(db_column='Gender', max_length=1)  # Field name made lowercase.
    primaryphysicianid = models.ForeignKey(Employees, models.DO_NOTHING,
                                           db_column='PrimaryPhysicianID')  # Field name made lowercase.
    medications = models.CharField(db_column='Medications', max_length=45, blank=True,
                                   null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'patient record'

    def __str__(self):
        return f"{self.lastname}, {self.firstname}"


class PharmacyOrder(models.Model):
    prescriptionid = models.IntegerField(db_column='PrescriptionID', primary_key=True)  # Field name made lowercase.
    patientid = models.ForeignKey(PatientRecord, models.DO_NOTHING, db_column='PatientID')  # Field name made lowercase.
    physicianid = models.ForeignKey(Employees, models.DO_NOTHING, db_column='PhysicianID')  # Field name made lowercase.
    medicationid = models.ForeignKey(Medication, models.DO_NOTHING,
                                     db_column='MedicationID')  # Field name made lowercase.
    dosage = models.CharField(db_column='Dosage', max_length=45, blank=True, null=True)  # Field name made lowercase.
    frequency = models.CharField(db_column='Frequency', max_length=45, blank=True,
                                 null=True)  # Field name made lowercase.
    date = models.DateField(db_column='Date', blank=True, null=True)  # Field name made lowercase.
    pharmacist = models.CharField(db_column='Pharmacist', max_length=45, blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'pharmacy order'


class Services(models.Model):
    serviceid = models.AutoField(db_column='ServiceID',
                                 primary_key=True)  # Field name made lowercase. The composite primary key (ServiceID, Cost) found, that is not supported. The first column is selected.
    description = models.CharField(db_column='Description', max_length=120, blank=True,
                                   null=True)  # Field name made lowercase.
    cost = models.FloatField(db_column='Cost')  # Field name made lowercase.

    class Meta:
        db_table = 'services'
        unique_together = (('serviceid', 'cost'),)


class Users(models.Model):
    username = models.CharField(db_column='Username', primary_key=True,
                                max_length=30)  # Field name made lowercase. The composite primary key (Username, EmployeeID) found, that is not supported. The first column is selected.
    employeeid = models.ForeignKey(Employees, models.DO_NOTHING, db_column='EmployeeID')  # Field name made lowercase.
    title = models.CharField(db_column='Title', max_length=20, blank=True, null=True)  # Field name made lowercase.
    password = models.CharField(db_column='Password', max_length=30)  # Field name made lowercase.
    firstname = models.CharField(db_column='FirstName', max_length=20)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=20)  # Field name made lowercase.

    class Meta:
        #
        db_table = 'users'
        unique_together = (('username', 'employeeid'),)
        db_table_comment = '\t'

class Vendor(models.Model):
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    equipment_types = models.CharField(max_length=200, help_text="Comma-separated list of equipment types")
    preferred = models.BooleanField(default=False)

    def str(self):
        return self.name

class ProblemType(models.Model):
    name = models.CharField(max_length=45, unique=True)

    def str(self):
        return self.name
    


