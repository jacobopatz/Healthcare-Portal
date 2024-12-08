from django.db import models

class Patient(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    date_of_birth = models.DateField()
    insurance_number = models.CharField(max_length=15, unique=True)
    carrier = models.ForeignKey('Carrier', on_delete=models.CASCADE, null=True, blank=True)  

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
class Carrier(models.Model):
    name = models.CharField(max_length=255, unique=True)
    address = models.TextField()
    payment_reliability = models.CharField(max_length=100, choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')])

    def __str__(self):
        return self.name


class Service(models.Model):
    id = models.AutoField(primary_key=True)
    description = models.CharField(max_length=255)
    billable_cost = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return self.description

class Billing(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    invoice_number = models.CharField(max_length=15, unique=True)
    invoice_date = models.DateField()
    service = models.ForeignKey(Service, on_delete=models.SET_NULL, null=True, blank=True)  # Link to Service
    service_description = models.TextField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_billed = models.DecimalField(max_digits=10, decimal_places=2)



class Invoice(models.Model):
    patient_name = models.CharField(max_length=255)
    carrier = models.ForeignKey(Carrier, on_delete=models.CASCADE, related_name='invoices')
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(max_length=100, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid'), ('pending', 'Pending')])
    issue_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Invoice {self.id} for {self.patient_name}"


