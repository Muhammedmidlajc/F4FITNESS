from django.shortcuts import render
from.models import*



def home(request):
    return render(request,"f4fitness/index.html",context={"data:data"})
    data=UserRegisteration.objects.all
    




# Create your views here.
