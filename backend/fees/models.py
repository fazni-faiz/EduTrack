from django.db import models
from students.models import Student

class FeePayment(models.Model):
    STATUS_CHOICES = (
        ('PAID', 'PAID'),
        ('PENDING', 'PENDING'),
    )

    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    month = models.CharField(max_length=20)  # "2025-01"
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    payment_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.student.full_name} - {self.month}"
