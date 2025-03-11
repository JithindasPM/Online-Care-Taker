from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from .forms import CustomLoginForm


from admins.forms import CustomUserCreationForm
from admins.forms import CustomLoginForm
from admins.forms import UserProfile_Form


from admins.models import UserProfile_Model
from admins.models import User


class Home(View):
    def get(self,request):
        return render(request,'index.html')
    
    
class Admin_View(View):
    def get(self,request):
        return render(request,'admin.html')


class RegisterView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'registration.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('login') 
        return render(request, 'registration.html', {'form': form})


class CustomLoginView(View):

    def get(self, request):
        form = CustomLoginForm()
        return render(request,'login.html', {'form': form})

    def post(self, request):
        form = CustomLoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                if user.is_superuser:
                    return redirect('admins')  
                elif user.user_type == 'customer':
                    return redirect('user') 
                elif user.user_type == 'service_provider':
                    return redirect('provider') 
                else:
                    messages.error(request, 'Invalid user type.')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            # Print form errors for debugging
            print(form.errors)

        return render(request, 'login.html', {'form': form})
    
    
class Logout_View(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home') 
    
class Update_UserProfile_View(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        data = UserProfile_Model.objects.get(id=id)
        form = UserProfile_Form(instance=data)
        return render(request, 'profile.html', {'form': form, 'data': data})

    def post(self, request, *args, **kwargs):
        id = kwargs.get('pk')
        data = UserProfile_Model.objects.get(id=id)
        form = UserProfile_Form(request.POST, request.FILES, instance=data)
        
        if form.is_valid():
            form.save()
            user_type = request.user.user_type

            if request.user.is_superuser:
                return redirect('admins')
            elif user_type == 'customer':
                return redirect('user')
            elif user_type == 'service_provider':
                return redirect('provider')

        return render(request, 'profile.html', {'form': form, 'data': data})

class All_provider_View(View):
    def get(self, request):
        providers = User.objects.filter(user_type='service_provider') 
        return render(request, 'all_provider.html', {'providers': providers})


from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden

class ToggleStatusView(View):
    
    def post(self, request, provider_id):
        # Allow only superusers to toggle status
        if not request.user.is_superuser:
            return HttpResponseForbidden("You are not allowed to perform this action.")

        # Fetch the profile and toggle status
        profile = get_object_or_404(UserProfile_Model, id=provider_id)
        profile.is_active = not profile.is_active
        profile.save()
        
        return redirect(request.META.get('HTTP_REFERER', 'home'))


