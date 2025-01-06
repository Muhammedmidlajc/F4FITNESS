from django.contrib import admin
from.models import*
from .models import UserProfile
from .models import TrainerProfile



admin.site.register(UserProfile)
admin.site.register(TrainerProfile)
