from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.cache import never_cache
from django.utils.decorators import method_decorator

from admins.models import Services_Model
from admins.models import Provider_Services_Model
from django.contrib import messages

from user.forms import ComplaintForm

# Create your views here.


from django.views import View
from django.shortcuts import render
from django.db.models import Sum, Count

from django.shortcuts import redirect
from functools import wraps

def service_provider_and_superuser_restriction(view_func):
    """
    Decorator to restrict access to views for users with user_type='service_provider'
    or superusers. Redirects them to the login page if they try to access a view.
    """
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        # Check if the user is authenticated and is a 'service_provider' or superuser
        if request.user.is_authenticated and (request.user.user_type == 'service_provider' or request.user.is_superuser):
            return redirect('login')  # Redirect to the login page if the user is a service provider or superuser
        return view_func(request, *args, **kwargs)
    
    return _wrapped_view





class User_View(LoginRequiredMixin,View):
    @method_decorator(service_provider_and_superuser_restriction)
    def get(self, request):
        user_bookings = Booking_Model.objects.filter(customer=request.user)

        total_bookings = user_bookings.count()

        pending_bookings = user_bookings.filter(status='pending').count()

        confirmed_bookings = user_bookings.filter(status='confirmed').count()

        context = {
            'total_bookings': total_bookings,
            'pending_bookings': pending_bookings,
            'confirmed_bookings': confirmed_bookings,
        }

        return render(request, 'user.html', context)

class ProvidersByServiceView(LoginRequiredMixin,View):
    template_name = 'all_services.html'
    @method_decorator(service_provider_and_superuser_restriction)
    def get(self, request, service_id):
        service = get_object_or_404(Services_Model, id=service_id)
        
        # Filter providers where the associated UserProfile is active
        providers = Provider_Services_Model.objects.filter(
            service=service,
            provider__userprofile_model__is_active=True
        )

        return render(request, self.template_name, {'service': service, 'providers': providers})


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import razorpay
from admins.models import Provider_Services_Model, Booking_Model

class User_Booking_List_View(LoginRequiredMixin, View):
    @method_decorator(service_provider_and_superuser_restriction)
    def get(self, request):
        bookings = Booking_Model.objects.filter(customer=request.user).order_by('-created_at')

        # Attach the provider's service amount and service name to each booking
        for booking in bookings:
            service = Provider_Services_Model.objects.filter(provider=booking.provider).first()
            booking.service_amount = service.amount if service else 0
            booking.service_name = service.service.name if service and service.service else "N/A"

        return render(request, 'user_bookings.html', {'bookings': bookings})


class Booking_Delete_View(LoginRequiredMixin, View):
    @method_decorator(service_provider_and_superuser_restriction)
    def get(self, request, *args,**kwargs):
        id=kwargs.get('pk')
        booking = get_object_or_404(Booking_Model, id=id)
        booking.delete()
        return redirect('user_bookings')
    
class Complaint_Register_View(LoginRequiredMixin,View):
    @method_decorator(service_provider_and_superuser_restriction)
    def get(self, request):
        form = ComplaintForm()
        return render(request, 'complaint.html', {'form': form})

    @method_decorator(service_provider_and_superuser_restriction)
    def post(self, request):
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user  
            complaint.save()
            form = ComplaintForm()
        return render(request, 'complaint.html', {'form': form})
    

razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class BookServiceView(LoginRequiredMixin, View):
    @method_decorator(service_provider_and_superuser_restriction)
    def get(self, request, provider_service_id):
        provider_service = get_object_or_404(Provider_Services_Model, id=provider_service_id)
        return render(request, 'booking_form.html', {'provider_service': provider_service})

    @method_decorator(service_provider_and_superuser_restriction)
    def post(self, request, provider_service_id):
        provider_service = get_object_or_404(Provider_Services_Model, id=provider_service_id)

        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')

        # Save booking details in session instead of creating a booking record now
        request.session['provider_service_id'] = provider_service.id
        request.session['booking_date'] = booking_date
        request.session['booking_time'] = booking_time

        # Create Razorpay Order
        amount = int(provider_service.amount * 100)  # Amount in paisa
        razorpay_order = razorpay_client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': '1'
        })

        context = {
            'order_id': razorpay_order['id'],
            'amount': amount,
            'provider_service': provider_service,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
        }

        return render(request, 'payment.html', context)



class PaymentSuccessView(View):
    @method_decorator(service_provider_and_superuser_restriction)
    def post(self, request):
        try:
            # Retrieve session data
            provider_service_id = request.session.get('provider_service_id')
            booking_date = request.session.get('booking_date')
            booking_time = request.session.get('booking_time')
            

            # Create booking only after successful payment verification
            provider_service = get_object_or_404(Provider_Services_Model, id=provider_service_id)
            booking = Booking_Model.objects.create(
                customer=request.user,
                provider=provider_service.provider,
                booking_date=booking_date,
                booking_time=booking_time,
            )

            # Clear session data
            del request.session['provider_service_id']
            del request.session['booking_date']
            del request.session['booking_time']
            del request.session['razorpay_order_id']

            messages.success(request, "Booking confirmed successfully!")
            return redirect('user')

        except Exception as e:
            return redirect('user')



