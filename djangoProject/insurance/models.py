from django.db import models

# Model for Insurance Carrier
class Carrier(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name


# Model for Patient
class patient(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    insurance_number = models.CharField(max_length=100, unique=True)
    carrier = models.ForeignKey(Carrier, related_name='patients', on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Model for Billing
class Billing(models.Model):
    patient = models.ForeignKey(patient, related_name='billings', on_delete=models.CASCADE)
    service_id = models.CharField(max_length=100, unique=True)
    service_description = models.CharField(max_length=255)
    date_of_service = models.DateField()
    amount_billed = models.DecimalField(max_digits=10, decimal_places=2)
    carrier = models.ForeignKey(Carrier, related_name='billings', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.service_description} - {self.date_of_service}"


# Model for Invoice
class Invoice(models.Model):
    billings = models.ManyToManyField(Billing, related_name='invoices')
    patient = models.ForeignKey(patient, related_name='invoices', on_delete=models.CASCADE)  # Link invoice to patient

    invoice_id = models.CharField(max_length=100, unique=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance_due = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_status = models.CharField(max_length=50, choices=[('Paid', 'Paid'), ('Unpaid', 'Unpaid')])

    def __str__(self):
        return f"Invoice {self.invoice_id} - {self.payment_status}"

    def calculate_totals(self):
        """Recalculate the total amount and balance due for the invoice."""
        total = sum([billing.amount_billed for billing in self.billings.all()])
        self.total_amount = total
        self.balance_due = total - self.amount_paid
        self.save()
