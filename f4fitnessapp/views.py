from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as login_user
from django.contrib import messages


def home(request):
    return render(request,"f4fitness/index.html")
from django.shortcuts import render, redirect
from .forms import UserProfileForm

# views.py
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserProfileForm

# views.py
from django.shortcuts import redirect
# views.py
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .forms import UserProfileForm

def register(request):
    if request.method == 'POST':
        form = UserProfile(request.POST, request.FILES)
        if form.is_valid():
            # Create a new User object first
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password']
            )

            # Save the UserProfile object but don't commit it yet
            user_profile = form.save(commit=False)
            user_profile.user = user  # Link the UserProfile to the User
            user_profile.save()  # Now save the UserProfile

            # Log the user in
            login(request, user)

            return redirect('f4fitness/login.html')  # Redirect to a success page
    else:
        form = UserProfileForm()
    
    return render(request, 'f4fitness/register.html', {'form': form})

# views.py
from django.shortcuts import render

def success(request):
    return render(request, 'f4fitness/success.html')

# views.py
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from .forms import LoginForm

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Authenticate user
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('success')  # Redirect to a success page after login
            else:
                form.add_error(None, "Invalid username or password")
    else:
        form = LoginForm()

    return render(request, 'f4fitness/login.html', {'form': form})