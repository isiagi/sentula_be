from saving.models import Saving
from loan.models import Loan
from payment.models import Payment
from userauth.models import CustomUser
from wagubumbuzi.models import Wagubumbuzi

MODEL_MAPPING = {
    'saving': Saving,
    'loan': Loan,
    'payment': Payment,
    'user': CustomUser,
    'wagumbulizi': Wagubumbuzi
    # Add more mappings as needed
}