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
    trainer = models.ForeignKey('TrainerProfile', on_delete=models.SET_NULL, null=True, blank=True, related_name="trainees")
    payment_expired=models.BooleanField(default=False)



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
    order=models.IntegerField(default=1)
    duration = models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"Session for {self.plan.Name} with {self.trainer.name}"

class SessionProgress(models.Model):
    user_session=models.ForeignKey('UserSession',on_delete=models.CASCADE)
    duration=models.IntegerField(default=0)


class UserSession(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    session = models.ForeignKey(Session, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    date_completed = models.DateTimeField(null=True,blank=True)
    order=models.IntegerField(default=1)
    status = models.CharField(max_length=50, choices=[('upcoming', 'Upcoming'), ('completed', 'Completed')], default='upcoming')

    def __str__(self):
        return f"Session {self.session.title} for {self.user.name} - Status: {self.status}"



class BuyHistory(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    supplements = models.ManyToManyField('ProductWithQuantity', blank=True)
    purchase_date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    payment_method = models.CharField(max_length=50, null=True, blank=True)  
    card_number = models.CharField(max_length=20, null=True, blank=True) 
    expiry_date = models.CharField(max_length=7, null=True, blank=True)  
    cvv = models.CharField(max_length=4, null=True, blank=True)  
    cardholder_name = models.CharField(max_length=100, null=True, blank=True)
    upi_id = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"BuyHistory for {self.user} on {self.purchase_date}"


class ProductWithQuantity(models.Model):
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    quantity=models.IntegerField(default=1)

    def __str__(self):
        return self.supplement.name
    

class BotData(models.Model):
    content=models.TextField()

class DietPlan(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True,blank=True)
    breakfast = models.TextField(default="🍳 Scrambled Eggs, 🥑 Avocado Toast, 🍓 Fresh Berries")
    lunch = models.TextField(default="🥗 Grilled Chicken Salad, 🍚 Quinoa, 🥕 Steamed Broccoli")
    dinner = models.TextField(default="🍣 Baked Salmon, 🥔 Mashed Sweet Potatoes, 🥦 Sautéed Spinach")
    snacks = models.TextField(default="🍌 Banana, 🥜 Almonds, 🍏 Apple Slices with Peanut Butter")


class WorkoutPlan(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True,blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    exercise_name = models.CharField(max_length=100)
    sets = models.IntegerField(default=3)
    repetitions = models.IntegerField(default=5)
    duration = models.IntegerField(default=30)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.exercise_name} - {self.user.name} ({self.date_created.strftime('%Y-%m-%d')})"


class Attendance(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,null=True,blank=True)
    date= models.DateField(null=True,blank=True) 
    status=models.BooleanField(default=False)

    def __str__(self):
        return f"Attendance for {self.user.name} on {self.date}"
    


class trainer_Attendance(models.Model):
    trainer = models.ForeignKey(TrainerProfile, on_delete=models.CASCADE,null=True,blank=True)
    date= models.DateField(null=True,blank=True) 
    status=models.BooleanField(default=False)

    def __str__(self):
        return f"Attendance for {self.trainer.name} on {self.date}"