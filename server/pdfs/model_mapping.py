from saving.models import Saving
from loan.models import Loan
from payment.models import Payment
from userauth.models import CustomUser

MODEL_MAPPING = {
    'saving': Saving,
    'loan': Loan,
    'payment': Payment,
    'user': CustomUser
    # Add more mappings as needed
}