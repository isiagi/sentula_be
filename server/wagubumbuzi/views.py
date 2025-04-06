from rest_framework.generics import ListAPIView, DestroyAPIView
from .models import Wagubumbuzi, WagubumbuziReduction
from .serializers import WagubumbuziSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .filters import WagubumbuziFilter
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum, F
from decimal import Decimal
from userauth.models import CustomUser



# Create your views here.
class WagubumbuziApiView(ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_class = WagubumbuziFilter


    serializer_class = WagubumbuziSerializer
    # queryset = Wagubumbuzi.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Wagubumbuzi.objects.all()
        return Wagubumbuzi.objects.filter(user=user)

class WagubumbuziDeleteApiView(DestroyAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = WagubumbuziSerializer
    queryset = Wagubumbuzi.objects.all()


# Get Amount from request and reduce from the wagubumbuzi total
class ReduceWagubumbuziApiView(ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAdminUser]


    def get(self, request, *args, **kwargs):
        # Get the current active reduction
        active_reduction = WagubumbuziReduction.get_active_reduction()
        
        # Get the current total of all Wagubumbuzi amounts
        total_current = Wagubumbuzi.get_total_amount()
        
        if active_reduction:
            response_data = {
                'total_current': float(total_current),
                'amount_reduced': float(active_reduction.amount_reduced),
                'total_after_reduction': float(active_reduction.total_after_reduction),
                'created_at': active_reduction.created_at,
                'updated_at': active_reduction.updated_at,
                'is_active': active_reduction.is_active
            }
        else:
            # No active reduction found
            response_data = {
                'total_current': float(total_current),
                'amount_reduced': 0.00,
                'total_after_reduction': float(total_current),
                'is_active': False
            }
            
        return Response(response_data, status=status.HTTP_200_OK)


    def post(self, request, *args, **kwargs):
        # Get the amount to reduce from the request
        amount_to_reduce = request.data.get('amount')

        # Validate input
        if not amount_to_reduce:
            return Response({
                'error': 'Amount is required'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convert amount to Decimal
            amount_to_reduce = Decimal(str(amount_to_reduce))
        except (ValueError, TypeError):
            return Response({
                'error': 'Invalid amount format'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total current amount

        total_current = Wagubumbuzi.get_total_amount()


        # Check if reduction is possible
        if total_current < amount_to_reduce:
            return Response({
                'error': 'Insufficient total amount to reduce'
            }, status=status.HTTP_400_BAD_REQUEST)


        # Create a new WagubumbuziReduction record
        reduction = WagubumbuziReduction(
            amount_reduced=amount_to_reduce
        )
        
        # Save the reduction (this will auto-calculate total_after_reduction)
        reduction.save()

        # Return the results
        return Response({
            'total_current': float(total_current),
            'total_after_reduction': float(reduction.total_after_reduction),
            'amount_reduced': float(reduction.amount_reduced),
            'created_at': reduction.created_at,
            'is_active': reduction.is_active

        }, status=status.HTTP_200_OK)