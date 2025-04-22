# wagubumbuzi/signals.py
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from decimal import Decimal
from .models import Wagubumbuzi, WagubumbuziReduction

@receiver(post_save, sender=Wagubumbuzi)
def create_reduction_on_save(sender, instance, created, **kwargs):
    """
    Signal to automatically create a new WagubumbuziReduction
    whenever a Wagumbuzi instance is created.
    """
    # Only run this for newly created instances
    if not created:
        return
    
    update_wagubumbuzi_reduction()

@receiver(post_delete, sender=Wagubumbuzi)
def update_reduction_on_delete(sender, instance, **kwargs):
    """
    Signal to automatically update WagubumbuziReduction
    whenever a Wagumbuzi instance is deleted.
    """
    update_wagubumbuzi_reduction()

def update_wagubumbuzi_reduction():
    """
    Helper function to update the WagubumbuziReduction based on current data.
    """
    try:
        # Get the total amount
        total_current = Wagubumbuzi.get_total_amount()
        
        # Get the active reduction to use its amount_reduced value
        active_reduction = WagubumbuziReduction.get_active_reduction()
        
        if active_reduction:
            # Use the amount_reduced from the active reduction
            reduction_amount = active_reduction.amount_reduced
        else:
            # If no active reduction exists, set a default value
            reduction_amount = Decimal('0.00')
        
        # Create a new WagubumbuziReduction record with the same amount_reduced
        reduction = WagubumbuziReduction(
            amount_reduced=reduction_amount
        )
        
        # Save the reduction (this will auto-calculate total_after_reduction)
        reduction.save()
        
        print(f"Reduction updated after Wagumbuzi change: {reduction_amount}")
    except Exception as e:
        # Log the error
        print(f"Error updating reduction: {str(e)}")