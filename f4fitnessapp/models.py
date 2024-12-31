from django.db import models
from django.contrib.auth.models import User
# models.py
# models.py# models.py
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    address = models.CharField(max_length=255, default='Unknown')
    username = models.CharField(max_length=50, unique=True)
    password = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/', null=True, blank=True)

    def __str__(self):
        return self.username

        

# class TrainerProfile(models.Model):
#     user = models.OneToOneField(User,on_delete=models.CASCADE)
#     phone_number = models.CharField(max_length=15,blank=True,null=True)
#     adress = models.TextField(blank=True,null=True)
#     date_of_birth = models.DateField(blank=True,null=True)
#     email=models.EmailField(blank=True,null=True)
#     qualification=models.TextField(blank=True,null=True)
#     experience=models.TextField(blank=True,null=True)

#     def __str__(self):
#         return self.user.first_name
    


# class userAttendance(models.Model):
#     user = models.ForeignKey(Userprofile,on_delete=models.CASCADE)
#     date=models.DateField()
#     is_attended=models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.user.user.first_name
    

# class TrainerAttendance(models.Model):
#     trainer = models.ForeignKey(TrainerProfile,on_delete=models.CASCADE)
#     date=models.DateField()
#     is_attended=models.BooleanField(default=False)
    
#     def __str__(self):
#         return self.trainer.user.first_name
    
# class Supplements(models.Model):
#     product_name = models.TextField(blank=True,null=True)
#     description = models.TextField(blank=True,null=True)
#     price = models.FloatField()
#     category =  models.TextField(blank=True,null=True)

 
#     def __str__(self):
#         return self.product_name
    
     