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
from admins.views import Home
from django.conf import settings  
from django.conf.urls.static import static 

from admins.views import Admin_View
from admins.views import CustomLoginView
from admins.views import RegisterView
from admins.views import Update_UserProfile_View
from admins.views import Logout_View
from admins.views import All_provider_View
from admins.views import ToggleStatusView


urlpatterns = [
    path('',Home.as_view(),name='home'),
    path('admins/',Admin_View.as_view(),name='admins'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('register/',RegisterView.as_view(),name='register'),
    path('profile/<int:pk>',Update_UserProfile_View.as_view(),name='profile'),
    path('logout',Logout_View.as_view(),name='logout'),
    path('all_providers/', All_provider_View.as_view(), name='all_providers'),
    path('toggle-status/<int:provider_id>/', ToggleStatusView.as_view(), name='toggle_status'),
    
    
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT) 
