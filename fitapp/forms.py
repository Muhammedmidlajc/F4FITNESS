from django import forms
from .models import UserProfile,plan
from .models import TrainerProfile





class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['name', 'dob', 'address', 'phone_number', 'image']
        widgets = {
            'password': forms.PasswordInput(),  
            'dob': forms.DateInput(attrs={'type': 'date'}), 
            'address': forms.Textarea(attrs={'rows': 3}),  
        }






class TrainerProfileForm(forms.ModelForm):
    class Meta:
        model = TrainerProfile
        fields = ['name',  'dob', 'address','phone_number','image','qualification', 'experience']
        widgets = {
            'password': forms.PasswordInput(),  
            'dob': forms.DateInput(attrs={'type': 'date'}), 
            'address': forms.Textarea(attrs={'rows': 3}),  
        }





from django import forms

class PlanForm(forms.ModelForm):
        class Meta:
            model = plan
            fields = '__all__'





from django import forms
from .models import Supplement

class SupplementForm(forms.ModelForm):
    class Meta:
        model = Supplement
        fields = ['name', 'price', 'description', 'image']








from .models import Payment

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['upi_id', 'amount']
        widgets = {
            'upi_id': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your UPI ID'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter the amount'}),
        }
