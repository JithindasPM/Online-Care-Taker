from django.views import View
from django.shortcuts import render, redirect
from django.contrib.auth import login,authenticate,logout
from .forms import CustomUserCreationForm
from django.contrib import messages
from .forms import CustomLoginForm
from django.core.paginator import Paginator
from django.views import View
from django.shortcuts import render
from django.utils import timezone


from admins.forms import CustomUserCreationForm
from admins.forms import CustomLoginForm
from admins.forms import UserProfile_Form
from admins.forms import Services_Form


from admins.models import UserProfile_Model
from admins.models import User
from admins.models import Services_Model
from admins.models import Booking_Model
from admins.models import Complaint_Model


class Home(View):
    def get(self,request):
        return render(request,'index.html')
    
    
class Admin_View(View):
    def get(self, request):
        # Total Customers
        total_customers = User.objects.filter(user_type='customer').count()
        
        # Active Service Providers
        active_agents = UserProfile_Model.objects.filter(
            user__user_type='service_provider',
            is_active=True
        ).count()
        
        # Bookings This Month
        now = timezone.now()
        bookings_this_month = Booking_Model.objects.filter(
            created_at__year=now.year,
            created_at__month=now.month
        ).count()
        

        context = {
            'total_customers': total_customers,
            'active_agents': active_agents,
            'bookings_this_month': bookings_this_month,
        }

        return render(request, 'admin.html', context)
    
# class Admin_View(View):
#     def get(self,request):
#         return render(request,'admin.html')


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

class All_Provider_View(View):
    def get(self, request):
        # Get all active service providers
        providers = User.objects.filter(
            user_type='service_provider',
        ).prefetch_related('provider_services_model_set')

        return render(request, 'all_provider.html', {'providers': providers})


from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden
from django.views import View
from django.contrib import messages

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponseForbidden

# class ToggleStatusView(View):
    
#     def post(self, request, provider_id):
#         # Allow only superusers to toggle status
#         if not request.user.is_superuser:
#             return HttpResponseForbidden("You are not allowed to perform this action.")

#         # Fetch the profile and toggle status
#         profile = get_object_or_404(UserProfile_Model, id=provider_id)
#         profile.is_active = not profile.is_active
#         profile.save()
        
#         return redirect(request.META.get('HTTP_REFERER', 'home'))



class ToggleStatusView(View):
    
    def post(self, request, provider_id):

        # Fetch the profile and toggle status
        profile = get_object_or_404(UserProfile_Model, id=provider_id)
        profile.is_active = not profile.is_active
        profile.save()

        # Prepare email content
        status = "activated" if profile.is_active else "deactivated"
        subject = "Account Status Update"
        message = f"Dear {profile.name},\n\nYour account has been {status} by the admin.\n\nRegards,\nAdmin Team"
        recipient = [profile.email]

        # Send email if the user has an email address
        if profile.email:
            try:
                send_mail(subject, message, None, recipient, fail_silently=False)
            except Exception as e:
                messages.error(request, f"Status changed but failed to send email: {e}")

        return redirect(request.META.get('HTTP_REFERER', 'home'))



class All_User_View(View):
    def get(self, request):
        providers = User.objects.filter(user_type='customer') 
        return render(request, 'all_users.html', {'providers': providers})
    
    
class Add_Service_View(View):
    template_name = 'services.html'

    def get(self, request):
        services=Services_Model.objects.all()
        form = Services_Form()
        return render(request, self.template_name, {'form': form,'services':services})

    def post(self, request):
        form = Services_Form(request.POST)
        if form.is_valid():
            form.save()
            form = Services_Form()
            services=Services_Model.objects.all()
            # return redirect('service') 
        return render(request, self.template_name, {'form': form,'services':services})
    
class Update_Service_View(View):
    template_name = 'services.html'

    def get(self, request, *args,**kwargs):
        id=kwargs.get('pk')
        data = get_object_or_404(Services_Model, id=id)
        form = Services_Form(instance=data)
        services=Services_Model.objects.all()
        return render(request, self.template_name, {'form': form, 'services': services})

    def post(self, request, *args,**kwargs):
        id=kwargs.get('pk')
        data = get_object_or_404(Services_Model, id=id)
        form = Services_Form(request.POST, instance=data)
        services=Services_Model.objects.all()
        if form.is_valid():
            form.save()
            return redirect('add_services')
        return render(request, self.template_name, {'form': form, 'services': services})
    
class Delete_Service_View(View):
    def get(self, request, *args,**kwargs):
        id=kwargs.get('pk')
        data = get_object_or_404(Services_Model, id=id)
        data.delete()
        return redirect('add_services') 


class Booking_Manage_View(View):
    def get(self, request):
        bookings_list = Booking_Model.objects.all().order_by('-created_at')  
        
        paginator = Paginator(bookings_list, 5)  
        page_number = request.GET.get('page')
        bookings = paginator.get_page(page_number)

        context = {
            'bookings': bookings,
        }
        return render(request, 'booking_manage.html', context)


class Complaint_List_View(View):
    def get(self, request):
        complaints = Complaint_Model.objects.all().order_by('-id')
        context = {
            'complaints': complaints
        }
        return render(request, 'all_complaint.html', context)
