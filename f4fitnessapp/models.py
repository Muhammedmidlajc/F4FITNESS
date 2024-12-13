from django.db import models
class GenderChoices(models.TextChoices):
    MALE="Male","Male"
    FEMALE="Female","Female"
    OTHER="Other","Other"





class UserRegisteration(models.Model):
    phone=models.CharField(max_length=12,null=True,blank=True)
    address=models.TextField(max_length=25)
    gender=models.CharField(max_length=6,choices=GenderChoices.choices)


    def __str__(self):
        return f' UserRegisteration{self.phone}'
        

