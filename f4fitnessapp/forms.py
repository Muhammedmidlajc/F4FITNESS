from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'date_of_birth', 'address', 'username', 'password', 'phone_number', 'image']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }




        # forms.py
from django import forms
from django.contrib.auth.forms import AuthenticationForm

class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget=forms.PasswordInput)


    # Optional: Add custom validation for password or username if needed




# class TrainerProfile(forms.ModelForm):
#      class Meta:
#         model = TrainerProfile
#         fields = [
#             'phone_number', 
#             'address', 
#             'date_of_birth', 
#             'email', 
#             'qualification', 
#             'experience'
#         ]