from django import forms
from .models import UserProfile
from .models import TrainerProfile





class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'username', 'password', 'dob', 'address', 'phone_number', 'image']
        widgets = {
            'password': forms.PasswordInput(),  
            'dob': forms.DateInput(attrs={'type': 'date'}), 
            'address': forms.Textarea(attrs={'rows': 3}),  
        }






class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ['name', 'username','password', 'dob', 'address','phone_number','image','qualification', 'experience']
        widgets = {
            'password': forms.PasswordInput(),  
            'dob': forms.DateInput(attrs={'type': 'date'}), 
            'address': forms.Textarea(attrs={'rows': 3}),  
        }










