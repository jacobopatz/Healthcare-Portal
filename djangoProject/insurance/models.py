from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    date_of_birth = models.DateField()
    insurance_number = models.CharField(max_length=15, unique=False)
    carrier_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=15, unique=True)
    invoice_date = models.DateField()
    service_id = models.CharField(max_length=15)
    service_description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_billed = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Invoice {self.invoice_number} for {self.patient}"


