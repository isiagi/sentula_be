from django.db import models
from decimal import Decimal
from django.db.models import Sum
from userauth.models import CustomUser
from decimal import Decimal


class Wagubumbuzi(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    saving_id = models.ForeignKey('saving.Saving', on_delete=models.CASCADE, blank=True, null=True)

    date_created = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"
    
    @classmethod
    def get_total_amount(cls):
        """Get the sum of all Wagubumbuzi amounts"""
        result = cls.objects.aggregate(total=Sum('amount'))
        return result['total'] or Decimal('0.00')


class WagubumbuziReduction(models.Model):
    amount_reduced = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_after_reduction = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Global Reduction: {self.amount_reduced}"
    
    def save(self, *args, **kwargs):
        # Calculate total_after_reduction based on all Wagubumbuzi records
        if self.is_active:
            # Deactivate any previously active reductions
            WagubumbuziReduction.objects.filter(is_active=True).exclude(pk=self.pk).update(is_active=False)
            
        # Get the sum of all Wagubumbuzi amounts
        total_amount = Wagubumbuzi.get_total_amount()
        
        # Calculate the total after reduction
        self.total_after_reduction = total_amount - self.amount_reduced
        
        # Ensure total_after_reduction is not negative
        if self.total_after_reduction < 0:
            self.total_after_reduction = Decimal('0.00')
            
        super().save(*args, **kwargs)
    
    @classmethod
    def get_active_reduction(cls):
        """Get the currently active reduction record"""
        try:
            return cls.objects.get(is_active=True)
        except cls.DoesNotExist:
            return None

