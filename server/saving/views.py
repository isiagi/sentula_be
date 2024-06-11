from datetime import datetime
from rest_framework.views import APIView
from wagubumbuzi.serializers import WagubumbuziSerializer
from wagubumbuzi.models import Wagubumbuzi 
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .serializers import SavingSerializer, SavingDataSerializer, SavingTotalSerializer
from .models import Saving
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .permissions import IsOwnerOrReadOnly
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models.functions import ExtractMonth, ExtractWeek, ExtractYear
from django.db.models import Sum
from django.db.models import Q

# Create your views here.

class GetSavingApiView(ListCreateAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    # queryset = Saving.objects.all()
    serializer_class = SavingSerializer

    # function to overide fetch
    def get_queryset(self):
        return Saving.objects.filter(user_id=self.request.user.id)
    
    # function to overide create
    def perform_create(self, serializer):
        user = self.request.user

        # user
        creating_user = serializer.validated_data['member_id']

        print(creating_user)

        # check if it's the first entry of the month
        today = datetime.now()
        first_of_month = today.replace(day=1, hour=0, minute=0,second=0, microsecond=0)

        if Saving.objects.filter(member_id=creating_user, date_of_payment__month=today.month).count() == 0:
            serializer.validated_data['amount'] = int(serializer.validated_data['amount']) - 5000

            # Save the Saving object
            saving_instance = serializer.save(user_id=user)

            cur = saving_instance.member_id

            print('cul', cur)

            # Add 5000 to wagubumbuzi
            wagubumbuzi_serializer = WagubumbuziSerializer(data={'user': cur, 'amount': 5000})

            if wagubumbuzi_serializer.is_valid():
                print("hello")
                wagubumbuzi_serializer.save(user=cur)
            else:
                saving_instance.delete()
                # wagubumbuzi_serializer.errors
                raise serializer.ValidationError("Failed to create wagubumbuzi object.")
        else:
            # save the Saving Object
            serializer.save(user_id=user)
        
    
        
# API route to handle PUT, PATCH, DELETE
class SavingDetailApiView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    queryset = Saving.objects.all()
    serializer_class = SavingSerializer

    def perform_update(self, serializer):
        # Fetch the new amount from the validated data
        new_amount = int(serializer.validated_data.get('amount', 0))
        
        # Deduct 5000 from the new amount
        updated_amount = new_amount - 5000
        
        # Update the amount in the validated data
        serializer.validated_data['amount'] = updated_amount
        
        # Save the updated object with the new amount
        serializer.save()  

    def perform_destroy(self, instance):        # Fetch the user associated with the instance
        user = instance.user_id

        print(user, 'user')

        # Check if it's the first entry of the month
        today = instance.date_of_payment
        if Saving.objects.filter(user_id=user, date_of_payment__month=today.month).count() == 1:
            # Delete all user Wagubumbuzi objects of that month
            Wagubumbuzi.objects.filter(
                user=user,
                date_created__year=today.year,
                date_created__month=today.month
            ).delete()

        # Proceed with the deletion of the Saving instance
        instance.delete()

# API route to handle GET Data Sum By week in a month
class GetSavingByWeekApiView(ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SavingDataSerializer

    def get_queryset(self):
        # Get the year and month from the URL
        month = self.kwargs.get('month')
        year = self.kwargs.get('year')

        # Get the data from the database
        data = Saving.objects.annotate(
            # Extract the year, month, and week from the date_of_payment
            year=ExtractYear('date_of_payment'),
            month=ExtractMonth('date_of_payment'),
            week=ExtractWeek('date_of_payment')
    
        ).filter(
            # Filter the data by year and month
            date_of_payment__year=year,
            date_of_payment__month=month
        ).values(
            # Group the data by year, month, and week
            'year', 'month', 'week' 
        ).annotate(
            # Sum the amount of each group
            count=Sum('amount')
        ).order_by(
            # Order in order below while returning
            'year', 'month', 'week'
        )

        return data
    

class GetSavingTotalApiView(ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = SavingTotalSerializer

    def get_queryset(self):
        data = Saving.objects.aggregate(Sum('amount'))

        return [data]

