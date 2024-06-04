from rest_framework import serializers
from django.contrib.auth.models import User

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class UserSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        fields = ['id','username', 'email', 'first_name', 'last_name','password'] 


class SignSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = User
        
        exclude = ('password','username',)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

class MemberSerializer(serializers.Serializer):
    membership_id = serializers.CharField()

    class Meta:
        fields = ['membership_id ']


class PasswordSerializer(serializers.Serializer):
    password = serializers.CharField()
    membership = serializers.CharField()

    class Meta:
        fields = ['password', 'membership']


class ResetPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(write_only=True)
    

    class Meta:
        fields = ['password']

    # Function validate passed data to the serializer
    def validate(self, data):
        # Get the passed password from the passed data.
        password = data.get('password')
        
        # Get passed Token from kwargs, for here url parameters
        token = self.context.get('kwargs').get('token')

         # Get passed encoded_pk from kwargs, for here url parameters
        encoded_pk = self.context.get('kwargs').get('encoded_pk')

        # Check if token and encoded_pk are present.
        if token is None or encoded_pk is None:
            # If not present send validation error
            raise serializers.ValidationError('Missing token or encoded_pk')
        
        # decrpty or decode encoded_pk back to normal id
        pk = urlsafe_base64_decode(encoded_pk).decode()

        # Get user object with matching id or primary key.
        user = User.objects.get(pk=pk)


        # Check if the sent token matches with the user object got from above
        # Token was created with a user, check is same user and real token
        if not PasswordResetTokenGenerator().check_token(user, token):
            # if not, sent validation error
            raise serializers.ValidationError('Invalid token')

        # set new password, this includes hashing the password
        user.set_password(password)

        # Save the user object in DB
        user.save()

        # Return serializer data.
        return data