from django.urls import path
from .views import WagubumbuziApiView

urlpatterns = [
    path('', WagubumbuziApiView.as_view(), name="wagubumbuzi_view"),
]