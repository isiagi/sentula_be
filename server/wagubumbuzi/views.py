from rest_framework.generics import ListAPIView, DestroyAPIView
from .models import Wagubumbuzi
from .serializers import WagubumbuziSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

# Create your views here.
class WagubumbuziApiView(ListAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]


    serializer_class = WagubumbuziSerializer
    # queryset = Wagubumbuzi.objects.all()

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Wagubumbuzi.objects.all()
        return Wagubumbuzi.objects.filter(user=user)

class WagubumbuziDeleteApiView(DestroyAPIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = WagubumbuziSerializer
    queryset = Wagubumbuzi.objects.all()
