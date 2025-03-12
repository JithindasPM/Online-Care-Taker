from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages


from admins.models import Provider_Services_Model
from provider.forms import Provider_Services_Form
# Create your views here.

class Provider_View(View):
    def get(self,request):
        return render(request,'provider.html')
    


class Add_Provider_Service_View(View):
    template_name = 'provider_service.html'

    def get(self, request):
        form = Provider_Services_Form()
        services = Provider_Services_Model.objects.filter(provider=request.user)
        return render(request, self.template_name, {'form': form, 'services': services})

    def post(self, request):
        form = Provider_Services_Form(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.provider = request.user 
            service.save()
            form = Provider_Services_Form()
        services = Provider_Services_Model.objects.filter(provider=request.user)
        return render(request, self.template_name, {'form': form, 'services': services})

class Update_Provider_Service_View(View):
    template_name = 'provider_service.html'

    def get(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        data = get_object_or_404(Provider_Services_Model, id=id)
        form = Provider_Services_Form(instance=data)
        services = Provider_Services_Model.objects.filter(provider=request.user)
        return render(request, self.template_name, {'form': form,'services':services})

    def post(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        data = get_object_or_404(Provider_Services_Model, id=id)
        form = Provider_Services_Form(request.POST, instance=data)
        if form.is_valid():
            form.save()
            services = Provider_Services_Model.objects.filter(provider=request.user)
            return redirect('provider_service')
        return render(request, self.template_name, {'form': form,'services':services})

class Delete_Provider_Service_View(View):
    def get(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        service = get_object_or_404(Provider_Services_Model, id=id)
        service.delete()
        return redirect('provider_service')

from admins.models import User
class Delete(View):
    def get(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        service = get_object_or_404(User, id=id)
        service.delete()



