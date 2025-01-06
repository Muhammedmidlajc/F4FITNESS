from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    username=models.CharField(max_length=60)
    password=models.CharField(max_length=50)
    dob = models.DateField(default='2000-01-01')
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/')
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png')




class TrainerProfile(models.Model):
    name = models.CharField(max_length=100, default='Trainer')

    username = models.CharField(max_length=60, default='default_username')

    password = models.CharField(max_length=50, default='defaultpassword')

    dob = models.DateField(default='2000-01-01')
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/', default='profile_images/default.png')
    qualification = models.TextField(blank=True, null=True)
    experience = models.TextField(blank=True, null=True)






    
