from django.shortcuts import render
from.models import*



def home(request):
    data=UserRegisteration.objects.all
    return render(request,"f4fitness/index.html",{'data':data})

    




# Create your views here.
