from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import PaymentSerializer
from .models import Payment

# Create your views here.

class PaymentApiView(ListCreateAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    # overide create operation
    def perform_create(self, serializer):
        # user = self.request.user

        # Save payment object, then used to access the foreign key obj, Loan obj
        # instance  with passed reference number.
        payment = serializer.save()

        # Access the payment key with foreign key value
        # This is done to gain access to the foreign key object, Loan with
        # the same reference_no has passed, and can be modified.
        loan = payment.reference

        # Modify the remaining_amount of foreign key object 
        loan.remaining_amount = float(loan.remaining_amount) - float(payment.amount)

        # Save the foriegn key instance with modifications.
        loan.save()


class PaymentDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.all()

    # Function to overide delete, this called when delete is fired.
    def perform_destroy(self, instance):
        # Get the current object to be deleted
        payment = Payment.objects.get(id=instance.id)

        # Access the reference key from the object, This gives us access to the
        # object of the foreign key instance,Loan current instance since it points to foreign.
        loan = payment.reference

        # Update remaining_amount of the foreign key, foreign obj.
        loan.remaining_amount = float(loan.remaining_amount) + float(payment.amount)

        # Save the foriegn key object, Loan object.
        loan.save()

        # delete payment
        payment.delete()