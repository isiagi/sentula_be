from django.urls import path
from . import views

urlpatterns =[

    path('staff-totals-pdf/', views.Staff_totals_pdf_view.as_view(), name='staff_totals_pdf'),
    path('<str:route>/', views.Get_Pdf.as_view(), name='pdfs'),

]