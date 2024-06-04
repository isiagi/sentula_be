"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from userauth import urls as auth_urls
from saving import urls as saving_urls
from wagubumbuzi import urls as wagubumbuzi_urls
from loan import urls as loan_urls
from payment import urls as payment_urls
from django.conf import settings
from userprofile import urls as profile_urls
from borrower import urls as borrower_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include(auth_urls)),
    path('api/saving/', include(saving_urls)),
    path('api/loan/', include(loan_urls)),
    path('api/payment/', include(payment_urls)),
    path('api/wagubumbuzi/', include(wagubumbuzi_urls)),
    path('api/user_profile/', include(profile_urls)),
    path('api/borrower/', include(borrower_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT,)
