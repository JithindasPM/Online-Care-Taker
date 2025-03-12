from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View

from admins.models import Services_Model
from admins.models import Provider_Services_Model


# Create your views here.


class User_View(View):
    def get(self,request):
        return render(request,'user.html')

class ProvidersByServiceView(View):
    template_name = 'all_services.html'

    def get(self, request, service_id):
        service = get_object_or_404(Services_Model, id=service_id)
        
        # Filter providers where the associated UserProfile is active
        providers = Provider_Services_Model.objects.filter(
            service=service,
            provider__userprofile_model__is_active=True
        )

        return render(request, self.template_name, {'service': service, 'providers': providers})
