from rest_framework import serializers
from django.contrib.auth.models import User
from userauth.models import CustomUser
from .models import Saving


class SavingSerializer(serializers.ModelSerializer):
    # setting the user_id to the id of the currently logged in user.
    # This also fires when creating, not sure
    user_id = serializers.PrimaryKeyRelatedField(queryset=CustomUser.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Saving
        fields = ['id','member_id', 'account_number', 'amount', 'date_of_payment', 'user_id', 'created_at', 'updated_at']
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Check if it's a GET request
        if self.context['request'].method == 'GET':
            self.Meta.depth = 1
        else:
            self.Meta.depth = 0  # Set depth to 0 for non-GET requests

class SavingDataSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    total_amount = serializers.IntegerField()


class SavingTotalSerializer(serializers.Serializer):
    amount__sum = serializers.CharField()
   