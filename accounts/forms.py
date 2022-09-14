from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile


class EnquiryForm(forms.Form):
    first_name = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    phone_number = forms.CharField(required=True)
    firm = forms.CharField(required=True)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()
 
    class Meta:
        model = User
        fields = ['username', 'email' , ]
 
 
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'addresses','pincode' , 'phone']    
          