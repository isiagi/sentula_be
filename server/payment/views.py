from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import PaymentSerializer
from .models import Payment
from rest_framework.exceptions import ValidationError

# Create your views here.

class PaymentApiView(ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Payment.objects.all()
        return Payment.objects.filter(user=user)

    # overide create operation
    def perform_create(self, serializer):
        # user = self.request.user

        # Save payment object, then used to access the foreign key obj, Loan obj
        # instance  with passed reference number.
        payment = serializer.save(penality=0)

        # Access the payment key with foreign key value
        # This is done to gain access to the foreign key object, Loan with
        # the same reference_no has passed, and can be modified.
        loan = payment.reference

        # Get loan user
        user = loan.user

        # print(user, 'user')
        payment.user = user

        payment.save()

        if float(loan.remaining_amount) - float(payment.amount) < 0:
            loan.loan_cost = 0
            #make positive
            loan.loan_cost = float(payment.amount) -float(loan.remaining_amount)
            loan.remaining_amount = 0 # Set remaining amount to 0


        else:
            loan.loan_cost = 0
            loan.remaining_amount = float(loan.remaining_amount) - float(payment.amount)

        # # Modify the remaining_amount of foreign key object 
        # loan.remaining_amount = float(loan.remaining_amount) - float(payment.amount)
        # # loan.remaining_amount = 0
        # loan.loan_cost = 0

        # Save the foriegn key instance with modifications.
        loan.save()


class PaymentDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    def perform_update(self, serializer):
        penality = serializer.validated_data.get('penality')

        if penality is not None:
            serializer.instance.penality = penality

            serializer.instance.save()
        else:
            raise ValidationError('penality is required')

    # Function to overide delete, this called when delete is fired.
    def perform_destroy(self, instance):
        # Get the current object to be deleted
        payment = Payment.objects.get(id=instance.id)

        # Access the reference key from the object, This gives us access to the
        # object of the foreign key instance,Loan current instance since it points to foreign.
        loan = payment.reference

        # Update remaining_amount of the foreign key, foreign obj.
        loan.remaining_amount = float(loan.remaining_amount) + float(payment.amount - loan.loan_cost)
        print(loan.remaining_amount, 'remaining_amount')

        # Update loan_cost
        loan.loan_cost = 0

        # Save the foriegn key object, Loan object.
        loan.save()

        # delete payment
        payment.delete()