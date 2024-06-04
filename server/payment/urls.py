from django.urls import path
from .views import PaymentApiView, PaymentDetailApiView

urlpatterns = [
    path("", PaymentApiView.as_view(), name="payment"),
    path("<int:pk>", PaymentDetailApiView.as_view(), name="payment"),
]