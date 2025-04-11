from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from rest_framework.authentication import TokenAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from .serializers import LoanSerializer, LoanTotalSerializer, LoanActiveSerializer, LoanDepthSerializer
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
from userauth.models import CustomUser
from .permissions import IsOwnerOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from wagubumbuzi.models import Wagubumbuzi
from rest_framework import filters
from django.utils import timezone
import datetime
# Create your views here.

@api_view(['GET'])
def get_reference_no(request):
    reference_no = Loan.objects.values_list('reference_no', flat=True)

    return Response(reference_no)


class GetLoanApiView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication, SessionAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    serializer_class = LoanSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['member_id', 'archived']  # Add archived to filterable fields
    ordering_fields = ['created_at']
    ordering = ['-created_at']

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return LoanDepthSerializer
        return LoanSerializer

    def get_queryset(self):
        user = self.request.user
        current_year = timezone.now().year

        print(self.request.query_params)
        
        # Get 'archived' parameter from request query params, default to showing current year loans
        show_archived = self.request.query_params.get('archived', 'false').lower() == 'true'

        print('hello')
        
        if user.is_staff:
            queryset = Loan.objects.all()
            print(queryset.count(), 'test man')
        else:
            queryset = Loan.objects.filter(user=user.id)
            
        # Filter based on year
        if show_archived:
            # Show loans from previous years (archived)
            print('archived reached')
            data = queryset.filter(created_at__year__lt=current_year)
            print(data.count(), 'test man here')

            return data
        else:
            # Show current year loans (default)
            return queryset.filter(created_at__year=current_year)

    # Function to generate unique loan reference
    def generate_unique_identifier(self, length=5, id='hello'):
        characters = string.digits
        identifier =''.join(random.choices(characters, k=length))

        return f"{id}/LN-{identifier}"

    # Overide create, This is called when creating
    def perform_create(self, serializer):
        membership_id = serializer.validated_data.get('member_id')

        user_is_borrower = get_object_or_404(Borrower, membership_id=membership_id)

        # Get user by membership_id
        user = user_is_borrower.membership_id

        print(user, 'user')


        # Generate unique code with this, self method / fx of class
        membership_id = serializer.validated_data.get('member_id')
        loan_reference = self.generate_unique_identifier(3, membership_id)

        # Get the amount passed from request and validated by serializer
        amount = serializer.validated_data.get('amount')

        # Save loan object while setting reference_no and remaining_amount manually
        serializer.save(user=user, reference_no=loan_reference, remaining_amount=amount)
        


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
        wagumbuzi = Wagubumbuzi.objects.aggregate(total_Wagubumbuzi = Sum('amount'))
        total_loan = queryset.aggregate(total_laon = Sum('amount'))
        total_cost = queryset.aggregate(total_cost = Sum('loan_cost'))
        total_remaining_amount = queryset.filter(remaining_amount__gt=0).aggregate(total_remaining_amount = Sum('remaining_amount'))
        count = queryset.filter(remaining_amount__gt=0).count()
        user_count = CustomUser.objects.count()

        data = {
            'total_laon': total_loan['total_laon'],
            'total_remaining_amount': total_remaining_amount['total_remaining_amount'],
            'total_cost': total_cost['total_cost'],
            'loan_count': count,
            'total_saving': savingset['total_saving'],
            'total_users': user_count,
            'total_wagubumbuzi': wagumbuzi['total_Wagubumbuzi']
        }

        return Response(data)
    



# TODO
# search fx