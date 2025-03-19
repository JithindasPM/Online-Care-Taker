from django.views import View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from admins.models import Booking_Model
from django.core.mail import send_mail, BadHeaderError
from django.contrib import messages
from django.conf import settings


from admins.models import Provider_Services_Model
from provider.forms import Provider_Services_Form
from django.db.models import Sum,Q

class Provider_View(LoginRequiredMixin, View):
    def get(self, request):
        latest_bookings = Booking_Model.objects.filter(
            Q(customer=request.user) | Q(provider=request.user)
        ).order_by('-created_at')[:2]
        
        bookings = Booking_Model.objects.filter(provider=request.user)

        total_bookings = bookings.count()
        
        booking_pending = bookings.filter(status='pending').count()
        
        booking_confirmed = bookings.filter(status='confirmed').count()

        context = {
            'total_bookings': total_bookings,
            'booking_pending': booking_pending,
            'booking_confirmed': booking_confirmed,
            'latest_bookings':latest_bookings
        }
        return render(request, 'provider.html', context)

    


class Add_Provider_Service_View(LoginRequiredMixin,View):
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

class Update_Provider_Service_View(LoginRequiredMixin,View):
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

class Delete_Provider_Service_View(LoginRequiredMixin,View):
    def get(self, request, *args, **kwargs):
        id=kwargs.get('pk')
        service = get_object_or_404(Provider_Services_Model, id=id)
        service.delete()
        return redirect('provider_service')


class Provider_Booking_View(LoginRequiredMixin, View):
    def get(self, request):
        bookings = Booking_Model.objects.filter(provider=request.user).order_by('-created_at')
        return render(request, 'provider_booking.html', {'bookings': bookings})

    def post(self, request):
        booking_id = request.POST.get('booking_id')
        new_status = request.POST.get('status')

        booking = get_object_or_404(Booking_Model, id=booking_id, provider=request.user)
        booking.status = new_status
        booking.save()

        # Check if the customer has an email
        recipient_email = booking.customer.email or getattr(booking.customer.userprofile_model, 'email', None)

        if recipient_email:
            subject = "Booking Status Update"
            message = (
                f"Hello {booking.customer.username},\n\n"
                f"Your booking for {booking.booking_date} at {booking.booking_time} "
                f"has been updated to '{new_status.title()}'.\n\n"
                "Thank you for choosing our service!"
            )
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [recipient_email])
                messages.success(request, "Booking status updated successfully and email sent to the user!")
            except BadHeaderError:
                messages.error(request, "Invalid header found in the email.")
            except Exception as e:
                messages.error(request, f"Failed to send email: {e}")
        else:
            messages.warning(request, "Booking status updated, but no email was sent (email not found).")

        return redirect('provider_booking')

