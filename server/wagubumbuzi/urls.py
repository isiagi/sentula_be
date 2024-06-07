from django.urls import path
from .views import WagubumbuziApiView, WagubumbuziDeleteApiView

urlpatterns = [
    path('', WagubumbuziApiView.as_view(), name="wagubumbuzi_view"),
    path('<int:pk>', WagubumbuziDeleteApiView.as_view(), name="wagubumbuzi_delete"),
]