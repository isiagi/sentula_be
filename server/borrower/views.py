from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .serializers import BorrowerSerializer
from .models import Borrower

# Create your views here.
class GetBorrowerApiView(ListCreateAPIView):
    serializer_class = BorrowerSerializer
    queryset = Borrower.objects.all()


class BorrowerDetailApiView(RetrieveUpdateDestroyAPIView):
    serializer_class = BorrowerSerializer
    queryset = Borrower.objects.all()