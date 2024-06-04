from rest_framework import serializers
from .models import Wagubumbuzi
from django.contrib.auth.models import User

# serializer to exclude some user fields when extracting user
class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        exclude = ('password','user_permissions', 'groups',)

class WagubumbuziSerializer(serializers.ModelSerializer):
    # Use of top serializer, added required and read_only to not use this
    # serializer with POST, PATCH, PUT
    user = UserSerializer(required=False, read_only=True)

    class Meta:
        model = Wagubumbuzi
        fields = '__all__'
        depth = 1