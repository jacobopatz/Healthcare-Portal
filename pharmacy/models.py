from django.db import models

class Prescription(models.Model):
    # Patient Information
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    patient_id = models.CharField(max_length=50)
    age = models.PositiveIntegerField()

    # Treatment Information
    medication = models.TextField()  # Store medication details as a JSON or text (e.g., serialized data)
    dosage = models.TextField()
    frequency = models.TextField()

    # Additional Information
    date_signed = models.DateField()
    signature = models.CharField(max_length=255)

    def __str__(self):
        return f"Prescription for {self.first_name} {self.last_name}"
    
class SummaryReport(models.Model):
    hospital_name = models.CharField(max_length=100)
    patient_name = models.CharField(max_length=100)
    birth_date = models.DateField()
    allergies = models.TextField(blank=True)
    address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    third_party_code = models.CharField(max_length=50)
    conditions = models.TextField(blank=True)
    
    # Prescription-specific fields
    prescription = models.ForeignKey('Prescription', on_delete=models.CASCADE)
    status = models.CharField(max_length=50)
    drug_quantity = models.IntegerField()
    dosage = models.CharField(max_length=50)
    date_issued = models.DateField()
    drug_code = models.CharField(max_length=50)
    directions = models.TextField()

    def __str__(self):
        return f"Summary Report for {self.patient_name} - {self.hospital_name}"

class Medication(models.Model):
    medication_name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=50)
    form_number = models.CharField(max_length=50)
    frequency = models.CharField(max_length=50)
    start_date = models.DateField(null=False, blank=False)
    end_date = models.DateField(null=True, blank=True)
    prescribing_doctor = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.medication_name