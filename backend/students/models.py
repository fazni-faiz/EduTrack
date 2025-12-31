from django.db import models
from batches.models import Batch

class Student(models.Model):
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=15)
    parent_phone = models.CharField(max_length=15)
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE)
    joined_date = models.DateField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.full_name

