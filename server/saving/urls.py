from django.urls import path
from .views import GetSavingApiView, SavingDetailApiView, GetSavingByWeekApiView, GetSavingTotalApiView

urlpatterns = [
    path('', GetSavingApiView.as_view(), name="saving_view"),
    path('<int:pk>', SavingDetailApiView.as_view(), name="saving_view"),
    path('data/<int:year>/<int:month>/', GetSavingByWeekApiView.as_view(), name='saving_data'),
    path('total/', GetSavingTotalApiView.as_view(), name='saving_total'),
]