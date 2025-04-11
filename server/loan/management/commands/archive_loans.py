from django.core.management.base import BaseCommand
from django.utils import timezone
from loan.models import Loan

class Command(BaseCommand):
    help = 'Archive loans from previous years'

    def handle(self, *args, **options):
        current_year = timezone.now().year
        
        # Get all loans from previous years that aren't already archived
        previous_year_loans = Loan.objects.filter(
            created_at__year__lt=current_year,
            archived=False
        )
        
        # Update them to be archived
        count = previous_year_loans.update(archived=True)
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully archived {count} loans from previous years.')
        )