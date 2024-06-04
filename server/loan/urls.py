from django.urls import path
from .views import GetLoanApiView, LoanDetailApiView, GetActiveLoanApiView,get_reference_no

urlpatterns = [
    path("", GetLoanApiView.as_view(), name="loan"),
    path("<int:pk>", LoanDetailApiView.as_view(), name="loan_detail"),
    # path("total", GetLoanTotalApiView.as_view(), name="loan_total"),
    path("active", GetActiveLoanApiView.as_view(), name="loan_active"),
    path("meta", get_reference_no, name="loan_meta"),
]