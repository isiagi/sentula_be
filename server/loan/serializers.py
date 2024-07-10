from rest_framework import serializers
from django.contrib.auth.models import User
from userauth.models import CustomUser
from .models import Loan
from borrower.serializers import CustomUserSerializer

class LoanSerializer(serializers.ModelSerializer):
    # Set user field to the current logged In user. 
    # user = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Loan
        fields = '__all__'
        extra_kwargs = {
            'remaining_amount': {'required': False},
        }
   
    def validate(self, data):
        if 'remaining_amount' not in data:
            data['remaining_amount'] = data.get('amount', 0)  # Default to amount if not provided
        return data

class LoanTotalSerializer(serializers.Serializer):
    amount__sum = serializers.IntegerField()


class LoanActiveSerializer(serializers.Serializer):
    total_remaining_amount = serializers.IntegerField()
    count_remaining_gt_Zero= serializers.IntegerField()

class LoanDepthSerializer(serializers.ModelSerializer):

    member_id = CustomUserSerializer(read_only=True)
    class Meta:
        model = Loan
        fields = '__all__'
        depth = 1  # Include depth

    def validate(self, data):
        if 'remaining_amount' not in data:
            data['remaining_amount'] = data.get('amount', 0)  # Default to amount if not provided
        return data

# 0726666256
# 0708930675(chosen)