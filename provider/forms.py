from django import forms
from admins.models import Provider_Services_Model

class Provider_Services_Form(forms.ModelForm):
    class Meta:
        model = Provider_Services_Model
        fields = ['service', 'description']
        widgets = {
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter service description',
                'rows': 3,  # Reduced number of rows
                'cols': 30  # Optional: Adjust width if needed
            }),
            'service': forms.Select(attrs={'class': 'form-control'}),
        }
  
  
      
        
        
        
        
        
        
        
        