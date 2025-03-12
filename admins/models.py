from django.contrib.auth.models import AbstractUser
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save

class User(AbstractUser):
    user_type = models.CharField(max_length=20, choices=[
        ('customer', 'Customer'),
        ('service_provider', 'Service Provider')
    ])

    def __str__(self):
        return self.username
    
class UserProfile_Model(models.Model):

    name=models.CharField(max_length=100,null=True)
    address=models.TextField(null=True)
    place = models.CharField(max_length=100)
    age=models.PositiveIntegerField(null=True)
    email=models.EmailField(null=True)
    profile_picture = models.ImageField(upload_to='images', blank=True, null=True)
    phone_number=models.CharField(max_length=15, null=True)
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    created_date=models.DateField(auto_now_add=True)  
    updated_date=models.DateField(auto_now=True)
    is_active=models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
@receiver(post_save,sender=User)
def create_profile(sender,instance,created,**kwargs):
        if created:      
            UserProfile_Model.objects.create(user=instance)
            
class Services_Model(models.Model):
    name=models.CharField(max_length=250)
    
    def __str__(self):
         return self.name
     
class Provider_Services_Model(models.Model):
    provider=models.ForeignKey(User,on_delete=models.CASCADE)
    service=models.ForeignKey(Services_Model,on_delete=models.CASCADE,null=True)
    description=models.TextField()
    created_date=models.DateField(auto_now_add=True)
    updated_date=models.DateField(auto_now=True)
    is_active=models.BooleanField(default=False)