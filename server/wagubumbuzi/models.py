from django.db import models
from saving.models import Saving
from userauth.models import CustomUser
from decimal import Decimal

class Wagubumbuzi(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_reduced = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'),
        blank=True
    )
    
    # Only for admin users
    total_after_reduction = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        default=Decimal('0.00'), 
        blank=True, 
        null=True
    )
    
    saving_id = models.ForeignKey(Saving, on_delete=models.CASCADE, blank=True, null=True)
    date_created = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"

    def save(self, *args, **kwargs):
        # Only set total_after_reduction for admin users
        if self.user and self.user.is_staff:
            if self.total_after_reduction is None:
                self.total_after_reduction = self.amount
        else:
            # Ensure non-admin users don't have this field set
            self.total_after_reduction = None
        
        super().save(*args, **kwargs)

    def clean(self):
        # Prevent non-admin users from setting total_after_reduction
        if self.user and not self.user.is_staff:
            self.total_after_reduction = None