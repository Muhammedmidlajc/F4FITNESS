from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    dob = models.DateField(default='2000-01-01')
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/')
    image1 = models.ImageField(upload_to='profile_images/', default='profile_images/default.png')




class TrainerProfile(models.Model):
    name = models.CharField(max_length=100, default='Trainer')
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    dob = models.DateField(default='2000-01-01')
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png')
    qualification = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)



class plan(models.Model):
    Name = models.CharField(max_length=25)
    time_period = models.CharField(max_length=25)
    price = models.CharField(max_length=25)
    descrption = models.CharField(max_length=100)
    


    
