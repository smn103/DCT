from django import forms
from django.contrib.auth.forms import UserCreationForm,UserChangeForm
from phone_field import PhoneField
from django.core.validators import RegexValidator
from django.forms.widgets import DateInput

from account.models import Account
from .models import Video

class RegistrationForm(UserCreationForm):
    phone_regex = RegexValidator(regex=r'^\d{10,10}$', message="Enter a 10 digit phone number")
    phone = forms.CharField(validators=[phone_regex], max_length=13) 

    class Meta:
        model=Account
        fields=("phone","username","email","password1","password2")

class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields= ["name","description" ,"video"]
        labels = {
        'name': ('Title')
        }

class EditProfileForm(UserChangeForm):
    password=None

    class Meta:
        model = Account
        fields = (
            'email',
            'first_name',
            'last_name',
            'bio',
            'website',
            'dob',
            'profile_pic',
            
            
        )
        labels = {
        'dob': ('Date of Birth'),
        'profile_pic':('Profile Picture')
        }
        widgets = {
        'dob': DateInput(attrs={'type': 'date'})
        }