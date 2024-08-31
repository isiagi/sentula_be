from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login, name='login'),
    path('member/', views.check_member, name='member'),
    path('users/', views.GetUsersApiView.as_view(), name='users'),
    path('totals/', views.GetTotalApiView.as_view(), name='totals'),
    path('meta/', views.get_membership_ids, name='meta'),
    path('meta/names/', views.get_members_names, name='meta_names'),
    path('get_password/', views.createpassword, name='password'),
    path('logout', views.logout, name='logout'),
    path('<int:pk>',views.UserDetailApiView.as_view(), name='user'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password/<str:encoded_pk>/<str:token>/', views.reset_password, name='reset_password'),
    path('validate_otp/', views.validate_otp, name='validate_otp'),
    path('delete_password/', views.deletepassword, name='delete_password'),
]