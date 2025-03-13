from django import forms
from admins.models import Complaint_Model

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint_Model
        fields = ['title', 'description']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter complaint title'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Describe your issue here', 
                'rows': 5  
            }),
        }
