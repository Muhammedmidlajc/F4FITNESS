from django.contrib import admin
from.models import*
from .models import UserProfile
from .models import TrainerProfile
from .models import plan,Supplement
from .models import Payment

admin.site.register(UserProfile)
admin.site.register(TrainerProfile)
admin.site.register(plan)
admin.site.register(Supplement)
admin.site.register(Payment)