from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import BorrowerSerializer, BorrowerGetSerializer
from .models import Borrower

# Create your views here.
class GetBorrowerApiView(ListCreateAPIView):
    
    queryset = Borrower.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return BorrowerGetSerializer
        return BorrowerSerializer


class BorrowerDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = BorrowerSerializer
    queryset = Borrower.objects.all()