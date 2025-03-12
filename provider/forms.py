from django import forms
from admins.models import Provider_Services_Model

class Provider_Services_Form(forms.ModelForm):
    class Meta:
        model = Provider_Services_Model
        fields = ['service', 'description', 'amount']  # Added 'amount' field
        widgets = {
            'service': forms.Select(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service description',
                'rows': 3,
                'cols': 30
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter service amount'
            }),
        }
  
  
      
        
        
        
        
        
        
        
        