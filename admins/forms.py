from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User


from admins.models import UserProfile_Model,Services_Model
from admins.models import Services_Model
from admins.models import Complaint_Model



class CustomUserCreationForm(UserCreationForm):
    user_type = forms.ChoiceField(
        choices=[('customer', 'Customer'), ('service_provider', 'Service Provider')],
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'user_type')


class CustomLoginForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Username',
        'class': 'form-control'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Password',
        'class': 'form-control'
    }))


class UserProfile_Form(forms.ModelForm):
    profile_picture = forms.ImageField(
        required=False,
        widget=forms.ClearableFileInput(attrs={'class': 'form-control'})
    )
    class Meta:
        model = UserProfile_Model
        fields = ['name','address','place','age','email','profile_picture','phone_number','bio']
        
        
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your name'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Enter your address', 'rows': 3}),
            'place': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your place'}),
            'age': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter your age'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter your email'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Tell us about yourself', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.required = True  # Make all fields required by default
        self.fields['profile_picture'].required = False  # Optional field
        self.fields['bio'].required = False  # Optional field


class Services_Form(forms.ModelForm):
    class Meta:
        model = Services_Model
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Service Name',
            }),
        }
        
from django import forms

class PasswordResetForm(forms.Form):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Enter your username',
        'class': 'form-control'
    }))

class OTPVerificationForm(forms.Form):
    otp = forms.CharField(widget=forms.NumberInput(attrs={
        'placeholder': 'Enter OTP',
        'class': 'form-control'
    }))


class SetNewPasswordForm(forms.Form):
    new_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter new password',
        'class': 'form-control'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm new password',
        'class': 'form-control'
    }))
