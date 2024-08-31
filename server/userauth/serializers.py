from rest_framework import serializers
from .models import CustomUser

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import re


class UserSerializer(serializers.ModelSerializer): 

    class Meta(object):
        model = CustomUser
        fields = ['id','username', 'email', 'first_name', 'last_name'] 
    
    def validate_username(self, value):
        # Custom validation logic for usernames in the format ADA/90826/2024
        if not re.match(r'^[A-Z]{3}/\d{3}/\d{4}$', value):
            raise serializers.ValidationError("Membership Id must be in the format ADA/000/2024")
        return value
    
    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        # instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance

class SignSerializer(serializers.ModelSerializer):

    class Meta(object):
        model = CustomUser
        
        exclude = ('password','username',)


class EmailSerializer(serializers.Serializer):
    email = serializers.EmailField()

    class Meta:
        fields = ['email']

class MemberSerializer(serializers.Serializer):
    membership_id = serializers.CharField()
    routeName = serializers.CharField()

    class Meta:
        fields = ['membership_id ', 'routeName']


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
        user = CustomUser.objects.get(pk=pk)


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
    

class EmailSendSerializer(serializers.Serializer):
    title= serializers.CharField()
    subject= serializers.CharField()
    message= serializers.CharField()

    class Meta:
        fields = ['title', 'subject', 'message']