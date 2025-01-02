from rest_framework.generics import ListAPIView, DestroyAPIView
from .models import Wagubumbuzi
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
        total_current = Wagubumbuzi.objects.aggregate(Sum('amount'))['amount__sum'] or Decimal('0')

        # Check if reduction is possible
        if total_current < amount_to_reduce:
            return Response({
                'error': 'Insufficient total amount to reduce'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Calculate total after reduction
        total_after_reduction = total_current - amount_to_reduce

        # Update all entries:
        # 1. Add the new reduction amount to amount_reduced
        # 2. Set total_after_reduction for admin users
        admin_users = CustomUser.objects.filter(is_staff=True)
        
        # Update all entries' amount_reduced
        Wagubumbuzi.objects.all().update(
            amount_reduced=F('amount_reduced') + (amount_to_reduce / Wagubumbuzi.objects.count())
        )

        # Update admin entries' total_after_reduction
        Wagubumbuzi.objects.filter(user__in=admin_users).update(
            total_after_reduction=total_after_reduction
        )

        # Return the results
        return Response({
            'total_after_reduction': float(total_after_reduction),
            'amount_reduced': float(amount_to_reduce)
        }, status=status.HTTP_200_OK)