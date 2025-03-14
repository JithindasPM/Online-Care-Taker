from django.shortcuts import render,redirect,get_object_or_404
from django.views.generic import View

from admins.models import Services_Model
from admins.models import Provider_Services_Model
from django.contrib import messages

from user.forms import ComplaintForm

# Create your views here.


from django.views import View
from django.shortcuts import render
from django.db.models import Sum, Count

class User_View(View):
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


from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.conf import settings
import razorpay
from admins.models import Provider_Services_Model, Booking_Model

# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.conf import settings
import razorpay

# Razorpay client initialization
razorpay_client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

class BookServiceView(LoginRequiredMixin, View):
    def get(self, request, provider_service_id):
        provider_service = get_object_or_404(Provider_Services_Model, id=provider_service_id)
        return render(request, 'booking_form.html', {'provider_service': provider_service})

    def post(self, request, provider_service_id):
        provider_service = get_object_or_404(Provider_Services_Model, id=provider_service_id)

        booking_date = request.POST.get('booking_date')
        booking_time = request.POST.get('booking_time')

        # Create booking with 'pending' status explicitly (even though it's the default)
        booking = Booking_Model.objects.create(
            customer=request.user,
            provider=provider_service.provider,
            booking_date=booking_date,
            booking_time=booking_time,
            status='pending'  # Explicitly set status to pending
        )

        # Create Razorpay Order
        amount = int(provider_service.amount * 100)  # Amount in paisa
        razorpay_order = razorpay_client.order.create({
            'amount': amount,
            'currency': 'INR',
            'payment_capture': '1'
        })

        # Save order and booking IDs in session for verification later
        request.session['booking_id'] = booking.id
        request.session['razorpay_order_id'] = razorpay_order['id']

        context = {
            'order_id': razorpay_order['id'],
            'amount': amount,
            'provider_service': provider_service,
            'razorpay_key': settings.RAZORPAY_KEY_ID,
            'booking_id': booking.id
        }

        return render(request, 'payment.html', context)


@method_decorator(csrf_exempt, name='dispatch')
class PaymentSuccessView(View):
    def post(self, request):
        booking_id = request.session.get('booking_id')
        if booking_id:
            booking = Booking_Model.objects.filter(id=booking_id).first()
            if booking:
                booking.save()
                return redirect('user') 
        return redirect('user')

class User_Booking_List_View(LoginRequiredMixin, View):
    def get(self, request):
        bookings = Booking_Model.objects.filter(customer=request.user).order_by('-created_at')

        # Attach the provider's service amount and service name to each booking
        for booking in bookings:
            service = Provider_Services_Model.objects.filter(provider=booking.provider).first()
            booking.service_amount = service.amount if service else 0
            booking.service_name = service.service.name if service and service.service else "N/A"

        return render(request, 'user_bookings.html', {'bookings': bookings})



class Booking_Delete_View(LoginRequiredMixin, View):

    def get(self, request, *args,**kwargs):
        id=kwargs.get('pk')
        booking = get_object_or_404(Booking_Model, id=id)
        booking.delete()
        return redirect('user_bookings')
    
    
class Complaint_Register_View(View):
    def get(self, request):
        form = ComplaintForm()
        return render(request, 'complaint.html', {'form': form})

    def post(self, request):
        form = ComplaintForm(request.POST)
        if form.is_valid():
            complaint = form.save(commit=False)
            complaint.user = request.user  
            complaint.save()
            form = ComplaintForm()
        return render(request, 'complaint.html', {'form': form})