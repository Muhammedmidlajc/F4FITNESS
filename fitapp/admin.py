from django.contrib import admin
from.models import*
from .models import UserProfile
from .models import TrainerProfile
from .models import plan,Supplement
from .models import Payment
from .models import CustomerOrder




admin.site.register(UserProfile)
admin.site.register(TrainerProfile)
admin.site.register(plan)
admin.site.register(Supplement)
admin.site.register(Payment)
admin.site.register(CustomerOrder)
admin.site.register(BuyHistory)
admin.site.register(ProductWithQuantity)
admin.site.register(Session)
admin.site.register(UserSession)
admin.site.register(SessionProgress)
