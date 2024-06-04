from rest_framework.generics import ListAPIView
from .models import Wagubumbuzi
from .serializers import WagubumbuziSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

# Create your views here.
class WagubumbuziApiView(ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]


    serializer_class = WagubumbuziSerializer
    queryset = Wagubumbuzi.objects.all()
