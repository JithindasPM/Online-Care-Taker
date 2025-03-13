"""
URL configuration for CareConnect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path,include
from provider.views import Provider_View
from provider.views import Add_Provider_Service_View
from provider.views import Update_Provider_Service_View,Provider_Booking_View
from provider.views import Delete_Provider_Service_View
from provider.views import Provider_Booking_View

urlpatterns = [
    path('provider/',Provider_View.as_view(),name='provider'),
    path('provider_service/',Add_Provider_Service_View.as_view(),name='provider_service'),
    path('update_provider_service/<int:pk>',Update_Provider_Service_View.as_view(),name='update_provider_service'),
    path('delete_provider_service/<int:pk>',Delete_Provider_Service_View.as_view(),name='delete_provider_service'),
    path('provider_booking',Provider_Booking_View.as_view(),name='provider_booking'),
    
    
]
