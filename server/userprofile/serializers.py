from rest_framework import serializers
from .models import UserProfile
from django.contrib.auth.models import User
from drf_extra_fields.fields import Base64ImageField
from userauth.models import CustomUser


# serializer to exclude some user fields when extracting user
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        exclude = ('password','user_permissions', 'groups',)




class UserProfileSerializer(serializers.ModelSerializer):
    # Use of top serializer, added required and read_only to not use this
    # serializer with POST, PATCH, PUT
    user = UserSerializer(required=False, read_only=True)
    # image_url = Base64ImageField()
    class Meta:
        model = UserProfile
        fields = '__all__'
        # depth of 1 to return the foreign key data instead of just id
        depth = 1