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

from user.views import User_View
from user.views import ProvidersByServiceView
from user.views import BookServiceView
from user.views import PaymentSuccessView
from user.views import User_Booking_List_View
from user.views import Booking_Delete_View


urlpatterns = [
    path('user/',User_View.as_view(),name='user'),
    path('providers/<int:service_id>/', ProvidersByServiceView.as_view(), name='providers_by_service'),
    path('book/<int:provider_service_id>/', BookServiceView.as_view(), name='book_service'),
    path('book-service/<int:provider_service_id>/', BookServiceView.as_view(), name='book_service_alt'),
    path('payment/success/', PaymentSuccessView.as_view(), name='payment_success'),
    path('user_bookings/', User_Booking_List_View.as_view(), name='user_bookings'),
    path('booking_delete/<int:pk>/', Booking_Delete_View.as_view(), name='booking_delete'),
    
    
]
