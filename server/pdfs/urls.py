from django.urls import path
from . import views

urlpatterns =[

    path('<str:route>/', views.Get_Pdf.as_view(), name='pdfs'),

]