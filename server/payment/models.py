from django.db import models
from loan.models import Loan

# Create your models here.

class Payment(models.Model):
    # to_field helps use another field instead of id of foreign key, default is id 
    # of foreign object
    reference = models.ForeignKey(Loan, to_field='reference_no', on_delete=models.CASCADE)
    payee = models.CharField(max_length=100)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)
    

    def __str__(self):
        return self.reference