from django.urls import path
from .views import UserProfileApiView, UserProfileDetailApiView, GetUserProfileApiView

urlpatterns = [
    path("", UserProfileApiView.as_view(), name="user_profile"),
    path("<int:pk>", UserProfileDetailApiView.as_view(), name="user_profile_details"),
    path("profile/<int:user_id>", GetUserProfileApiView.as_view(), name="get_user_profile_details")
]