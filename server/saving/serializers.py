from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Saving


class SavingSerializer(serializers.ModelSerializer):
    # setting the user_id to the id of the currently logged in user.
    # This also fires when creating, not sure
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), default=serializers.CurrentUserDefault())

    class Meta:
        model = Saving
        fields = ['id','member_id', 'member_name', 'account_number', 'amount', 'date_of_payment', 'user_id', 'created_at', 'updated_at']

class SavingDataSerializer(serializers.Serializer):
    year = serializers.IntegerField()
    month = serializers.IntegerField()
    week = serializers.IntegerField()
    count = serializers.IntegerField()


class SavingTotalSerializer(serializers.Serializer):
    amount__sum = serializers.CharField()
   