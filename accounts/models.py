
from django.db import models
from django.contrib.auth.models import User
from PIL import Image
 
 
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    addresses =models.CharField(max_length=200,null=True, blank=True)
    pincode =models.CharField(max_length=6,null=True, blank=True)
    phone =models.CharField(max_length=13,null=True, blank=True)

    
 
    def __str__(self):
        return f'{self.user.username} Profile'

# Create your models here.
class Enquiry(models.Model):
    
    name = models.CharField(max_length=121)
    email = models.CharField(max_length=121)
    firm  = models.CharField(max_length=111)
    date = models.DateField()
 
    def __str__(self):
      return self.name