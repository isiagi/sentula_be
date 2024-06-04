from django.urls import path
from . import views

# url patterns

urlpatterns = [
    path("", views.GetBorrowerApiView.as_view(), name="borrower_list"),
    path("<int:pk>", views.BorrowerDetailApiView.as_view(), name="borrower_detail"),
]