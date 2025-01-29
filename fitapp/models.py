from django.db import models
from django.contrib.auth.models import User



class UserProfile(models.Model):
    name = models.CharField(max_length=100)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True,blank=True)
    plan = models.ForeignKey('plan', on_delete=models.CASCADE,null=True,blank=True)
    dob = models.DateField(default='2000-01-01')
    address = models.TextField()
    phone_number = models.CharField(max_length=15)
    image = models.ImageField(upload_to='profile_images/')
    image1 = models.ImageField(upload_to='profile_images/', default='profile_images/default.png')
    paid=models.BooleanField(default=False)



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
    Type = models.CharField( max_length=50,blank=True, null=True)
    
    def __str__(self):
        return self.Name
    

class Supplement(models.Model):
    name = models.CharField(max_length=100, unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='supplements/images/', blank=True, null=True)

    






class Payment(models.Model):
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True,blank=True)
    upi_id = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.id} - {self.upi_id} - {self.amount}"




class CustomerOrder(models.Model):
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    address = models.TextField()
    upi_id = models.CharField(max_length=255, blank=True, null=True)  # Added this line
    payment_mode = models.CharField(max_length=50)
    product = models.ForeignKey('Supplement', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.name


class Session(models.Model):
    title=models.CharField(max_length=255,null=True,blank=True)
    plan = models.ForeignKey('Plan', on_delete=models.CASCADE)
    trainer = models.ForeignKey('TrainerProfile', on_delete=models.CASCADE,null=True,blank=True)
    time = models.CharField(max_length=100,null=True,blank=True)
    duration = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"Session for {self.plan.Name} with {self.trainer.name}"
