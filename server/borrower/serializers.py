from rest_framework import serializers
from .models import Borrower
from userauth.serializers import UserSerializer
from userauth.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        exclude = ['password', 'user_permissions', 'groups', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'date_joined', 'otp', 'id']

class BorrowerGetSerializer(serializers.ModelSerializer):
    membership_id = CustomUserSerializer(read_only=True)

    class Meta:
        model = Borrower
        fields = '__all__'
        depth = 1  # You can set the depth if needed

class BorrowerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrower
        fields = '__all__'