from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import LoanSerializer, LoanTotalSerializer, LoanActiveSerializer
from .models import Loan
import random
import string
from django.db.models import Sum, Count, Q
from rest_framework.response import Response
from rest_framework.decorators import api_view
from saving.models import Saving
from django.contrib.auth.models import User
from borrower.models import Borrower
from django.shortcuts import get_object_or_404

# Create your views here.

@api_view(['GET'])
def get_reference_no(request):
    reference_no = Loan.objects.values_list('reference_no', flat=True)

    return Response(reference_no)


class GetLoanApiView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()

    # Function to generate unique loan reference
    def generate_unique_identifier(self, length=5, id='hello'):
        characters = string.digits
        identifier =''.join(random.choices(characters, k=length))

        return f"{id}/LN-{identifier}"

    # Overide create, This is called when creating
    def perform_create(self, serializer):
        membership_id = serializer.validated_data.get('member_id')

        user_is_borrower = get_object_or_404(Borrower, membership_id=membership_id)


        # Generate unique code with this, self method / fx of class
        membership_id = serializer.validated_data.get('member_id')
        loan_reference = self.generate_unique_identifier(3, membership_id)

        # Get the amount passed from request and validated by serializer
        amount = serializer.validated_data.get('amount')

        # Save loan object while setting reference_no and remaining_amount manually
        serializer.save(reference_no=loan_reference, remaining_amount=amount)
        


class LoanDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = LoanSerializer
    queryset = Loan.objects.all()



# class GetLoanTotalApiView(ListAPIView):
#     authentication_classes = [SessionAuthentication, TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     serializer_class = LoanTotalSerializer

#     def get_queryset(self):
#         data = Loan.objects.aggregate(Sum('amount'))

#         return [data]
    

class GetActiveLoanApiView(ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = LoanActiveSerializer

    def list(self, request, *args, **kwargs):
        queryset = Loan.objects.all()
        savingset = Saving.objects.aggregate(total_saving = Sum('amount'))
        total_loan = queryset.aggregate(total_laon = Sum('amount'))
        total_remaining_amount = queryset.filter(remaining_amount__gt=0).aggregate(total_remaining_amount = Sum('remaining_amount'))
        count = queryset.filter(remaining_amount__gt=0).count()
        user_count = User.objects.count()

        data = {
            'total_laon': total_loan['total_laon'],
            'total_remaining_amount': total_remaining_amount['total_remaining_amount'],
            'loan_count': count,
            'total_saving': savingset['total_saving'],
            'total_users': user_count
        }

        return Response(data)
    



# TODO
# search fx