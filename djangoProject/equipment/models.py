from django.db import models
from django.utils.timezone import now 
import uuid

#BE VERY CAUTIOUS OF META NAMES, THE SHAREDMODELS OF THESE AREN'T DELETED

class Vendor(models.Model):
    vendorid = models.IntegerField(db_column='VendorID', primary_key=True)
    name = models.CharField(max_length=100, unique=True)
    address = models.TextField()
    equipment_types = models.CharField(max_length=200, help_text="Comma-separated list of equipment types")
    preferred = models.BooleanField(default=False)

    class Meta:
        db_table = 'vendor'

    def str(self):
        return self.name

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
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, null=True, blank=True)
    class Meta:
        db_table = 'equipment_two'

# Create your models here.
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
        db_table = 'maintenance_two'
        unique_together = (('maintenanceid', 'equipmentid'),)

class ProblemType(models.Model):
    name = models.CharField(max_length=45, unique=True)

    def str(self):
        return self.name