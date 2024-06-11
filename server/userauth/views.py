from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.contrib.auth.models import User
from rest_framework.response import Response
from .serializers import UserSerializer, EmailSerializer, ResetPasswordSerializer, PasswordSerializer, MemberSerializer, SignSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authtoken.models import Token

from rest_framework import status
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from django.urls import reverse
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from rest_framework.generics import ListAPIView, RetrieveUpdateDestroyAPIView, DestroyAPIView

from .email_service import send
from userprofile.models import UserProfile
import random
import string
from datetime import datetime
from .models import CustomUser

from django.db.models import Sum

from saving.models import Saving
from loan.models import Loan
from borrower.models import Borrower
from payment.models import Payment
from wagubumbuzi.models import Wagubumbuzi


# Users 
# @api_view(['GET'])
# def getUsers(request):
#     User = get_user_model()
#     user = User.objects.all()

#     serializer = UserSerializer(data=user)

#     all_users = User.objects.values()

#     return Response({"users": all_users}, status=status.HTTP_200_OK)

class GetUsersApiView(ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        User = get_user_model()
        user = CustomUser.objects.all()

        return CustomUser.objects.values()
    
class UserDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    queryset = CustomUser.objects.all()

class UserDeleteApi(DestroyAPIView):
   queryset = CustomUser.objects.all()
   serializer_class = UserSerializer

# Login View
@api_view(['POST'])
def login(request):
    # check if user exists or raise exception with 404
    user = get_object_or_404(CustomUser, username = request.data['Member_Id'])

    # check if database password & provided password match
    if not user.check_password(request.data['Password']):
        return Response({"message": "User or Password Invalid"}, status = status.HTTP_404_NOT_FOUND)
    
    print("user", user.pk)

    # Serializer data sent by useTypeError: Object of type User is not JSON serializabler
    serializer = UserSerializer(instance=user)

    print("userweeweew", serializer.data)
    
    # get or create auth Token
    token, created = Token.objects.get_or_create(user=user)

    # Serializer data sent by user
    # serializer = UserSerializer(instance=user)

    # Response
    return Response({'message': 'User Logined In', 'Token': token.key, 'User': serializer.data}, status = status.HTTP_200_OK)



# Sign Up
@api_view(['POST'])
def signup(request):
    # serializer user data
    serializer = SignSerializer(data=request.data)

    # Generate membership identifier
    def generate_unique_identifier(length=5):
        characters = string.digits
        identifier =''.join(random.choices(characters, k=length))

        today = datetime.now()

        return f"ADA/{identifier}/{today.year}"
    
    # Get username from request data
    membership_id = request.data.get('username')

    # Valid ID
    valid_id = f"ADA/{membership_id}"

    # check serialization valid
    if serializer.is_valid():
        # save user data to database
        try:
            CustomUser.objects.get(username = valid_id)
            return Response({"detail": 'Membership Id already exists'}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            pass

        # save user
        tst = serializer.save(username=valid_id, password="")

        # create profile with saved user
        UserProfile.objects.create(user=tst)

        # check for user in DB and hash password.
        # user = User.objects.get(username = request.data.get('username'))

        # hash password
        # user.set_password(request.data.get('password'))

        # save user with hashed password
        # user.save()

        # create Auth Token
        # token = Token.objects.create(user=user)

        # Response if everything Okay
        return Response({'message': "User Signed up successfully", "User": serializer.data, "membership_id": tst.username}, status=status.HTTP_201_CREATED)
    
    # Throw error if serialization of data fails
    return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def check_member(request):
    serializer = MemberSerializer(data=request.data)

    if serializer.is_valid():
        user = CustomUser.objects.get(username = request.data['membership_id'], password = "")

        if not user or user == None:
            return Response({"Error": 'Membership Id not found'}, status=status.HTTP_400_BAD_REQUEST)
        else:
           # Response if everything Okay
            return Response({'message': "User Found",  "User": serializer.data}, status=status.HTTP_200_OK) 
        
    else:
        # Throw error if serialization of data fails
        return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    

@api_view(['GET'])
def get_membership_ids(request):
    membership_ids = CustomUser.objects.values_list('username', flat=True)

    return Response(membership_ids)

def combine_names(data):
    if isinstance(data, list) and all(isinstance(item, dict) for item in data):
        combined_names = []
        for item in data:
            first_name = item.get('first_name', '').strip()
            last_name = item.get('last_name', '').strip()
            if first_name or last_name:  # Skip if both are empty
                full_name = f"{first_name} {last_name}".strip()
                combined_names.append(full_name)
        return combined_names
    return data

@api_view(['GET'])
def get_members_names(request):
    members = CustomUser.objects.all().values('first_name', 'last_name')

    combined_members = combine_names(list(members))

    return Response(combined_members)


@api_view(['POST'])
def createpassword(request):
    serializer = PasswordSerializer(data=request.data)

    if serializer.is_valid():
        # check for user in DB and hash password.
        user = CustomUser.objects.get(username = request.data['membership'])

        # Hash and Set Password
        user.set_password(request.data['password'])

        # Save user
        user.save()

        token = Token.objects.create(user=user)

        nv = UserSerializer(user)

        # Response if everything Okay
        return Response({'message': "User Password Set",'token': token.key,  "User": nv.data}, status=status.HTTP_201_CREATED)
    else:
        # Throw error if serialization of data fails
        return Response({"Error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

# Logout
@api_view(['POST'])
@authentication_classes([SessionAuthentication, TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout(request):
    # delete token
    request.user.auth_token.delete()

    # Response
    return Response({"message": "User Logged Out"}, status=status.HTTP_200_OK)





@api_view(['POST'])
def forgot_password(request):
    # Deserialize request data,
    serializer = EmailSerializer(data=request.data)

    # Check if data is valid, matching the model / serializer requirements
    serializer.is_valid(raise_exception=True)

    # Access the email from pass data from the request
    email = request.data['email']

    print("email", email)
    
    # Find the first entry of the email from the user table
    user = CustomUser.objects.filter(email=email).first()

    if user:
        # Make encrptyed text for the user id
        encoded_pk = urlsafe_base64_encode(force_bytes(user.pk))

        # Generate Token with user object
        token = PasswordResetTokenGenerator().make_token(user)

        # User reverse to get url path of url with name 'reset_password' in url file
        # And passing some data along matching the url

        reset_url = reverse('reset_password', kwargs={'encoded_pk': encoded_pk, 'token': token})

        # Make reset Link
        reset_link = f"http://127.0.0.1:8000{reset_url}"

        # Send reset link by email.
        send('Reset Password Link', reset_link, [email])

        return Response({"message": "Password reset link sent to your email"}, status=status.HTTP_200_OK)
    
    return Response({"message": "User not found"}, status=status.HTTP_404_NOT_FOUND)


@api_view(['PATCH'])
def reset_password(request, *args, **kwargs):
    # Deserialize request data,
    serializer = ResetPasswordSerializer(data=request.data, context={'kwargs': kwargs})

      # Check if data is valid
    serializer.is_valid(raise_exception=True)

    return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)


class GetTotalApiView(ListAPIView):
    serializer_class = MemberSerializer
    queryset = CustomUser.objects.all()

    def list(self, request, *args, **kwargs):
        queryset = CustomUser.objects.all()
        borrowerset = Borrower.objects.all().count()
        total = queryset.count()
        savingset = Saving.objects.aggregate(total_saving = Sum('amount'))
        total_loan = Loan.objects.aggregate(total_laon = Sum('amount'))
        total_payment = Payment.objects.aggregate(total_payment = Sum('amount'))
        total_wagubumbuzi = Wagubumbuzi.objects.aggregate(total_Wagubumbuzi = Sum('amount'))

        data = {
            'totalMembers': total,
            'total_saving': savingset,
            'total_laon': total_loan,
            'total_payment': total_payment,
            'total_wagubumbuzi': total_wagubumbuzi,
            'total_borrower': borrowerset
        }

        return Response(data)
    
