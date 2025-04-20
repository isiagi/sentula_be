
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView
from .serializers import UserProfileSerializer
from .models import UserProfile
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from .permissions import IsOwnerOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

# Create your views here.

class UserProfileApiView(ListCreateAPIView):
    # Authentication And Permission Class
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # Parser Class - form data - images
    parser_classes=(MultiPartParser, FormParser, JSONParser)

    # Serializer class and Queryset
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    # Overide creating, runs when creating instance
    def perform_create(self, serializer):
        # Save this object with user key as the id of the logined user
        return serializer.save(user=self.request.user)

    

# Route to update user profile 
class UserProfileDetailApiView(RetrieveUpdateDestroyAPIView):
    # Authentication And Permission Class
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # Parser Class - form data - images
    parser_classes=(MultiPartParser, FormParser, JSONParser)

    # Serializer class and Queryset
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    # This runs during updating of the object
    def perform_update(self, serializer):
        # Get object to be updated
        instance = self.get_object()

        # Access user using foreign key user in the profile obj
        user = instance.user

        # Update user data from the profile route.
        user.last_name = self.request.data.get('last_name')
        user.first_name = self.request.data.get('first_name')
        user.email = self.request.data.get('email')
        
        # If the user is staff, allow changing is_staff status
        if self.request.user.is_staff:
            # Convert string representation to boolean
            is_staff_value = self.request.data.get('is_staff')
            if isinstance(is_staff_value, str):
                # Convert string to boolean properly
                is_staff_value = is_staff_value.lower() == 'true'
            
            user.is_staff = is_staff_value if is_staff_value is not None else user.is_staff
        
        # Save user model
        user.save()

        # Save Userprofile model
        return serializer.save()
    

# Route to get user profile by user id
class GetUserProfileApiView(ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    # Serializer class and Queryset
    serializer_class = UserProfileSerializer
    queryset = UserProfile.objects.all()

    def get_queryset(self):
        # Pick user id from the url params
        user_id = self.kwargs.get('user_id')
        # Return objects where field user = user id from params
        return self.queryset.filter(user=user_id)


# TODOS 
# Delete images from server
# Find profile by userId or pk, only work for admins
# One user can have on profile
# Create profile on creating user