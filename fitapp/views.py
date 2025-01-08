from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import UserProfileForm
from .forms import TrainerProfileForm
from. import views
from.models import TrainerProfile
from django.shortcuts import get_object_or_404
from.models import UserProfile
from django.contrib.auth.models import User








def home(request):
    return render(request, "f4fitness/index.html")

def trainer_management(request):
    trainers = TrainerProfile.objects.all()
    return render(request, "trainer.html",{'trainers':trainers})



def register(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        username=request.POST.get('username')
        password=request.POST.get('password')

        if form.is_valid():
                try:
                    user=User.objects.create_user(username=username,password=password)
                except Exception as e:
                    print(e)
                    render(request, 'f4fitness/register.html', {'form': form})
                profile=form.save(commit=False)
                profile.user=user
                profile.save()

                messages.success(request, 'Registration successful! Please login.')
                return redirect('login')  
    else:
        form = UserProfileForm()

    return render(request, 'f4fitness/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        print(username,password,user)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('user_dashboard')
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('login')  

    return render(request, 'f4fitness/login.html')


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('login')

def user_profile(request):
    profile = get_object_or_404(UserProfile, user=request.user)

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        name = request.POST.get('name')
        dob = request.POST.get('dob')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        image = request.FILES.get('image')

        # Update user model
        if username :
            request.user.username = username
        if password:
            request.user.set_password(password)
        request.user.save()

        # Update user profile
        profile.name = name
        profile.dob = dob
        profile.address = address
        profile.phone_number = phone_number
        if image:
            profile.image = image
        profile.save()

        messages.success(request, 'Profile updated successfully!')
        return redirect('user_profile')

    return render(request, 'userprofile.html', {'profile': profile})


def user_progress(request):
    profile = get_object_or_404(UserProfile, user=request.user)
    return render(request, 'user_progress.html', {'profile': profile})

from django.http import JsonResponse
import json

def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body) 
        user_message = data.get('message') 
        bot_response = "This is a placeholder response." 
        print(user_message)
        if user_message == 'hii':
            bot_response = 'helllo'
        return JsonResponse({'response': bot_response})
    return render(request, 'chatbot.html')





USERNAME='fitness'
PASSWORD='12345'
def admin_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username==USERNAME and password==PASSWORD:
            return redirect('admin_dashboard')
        else:
            messages.error(request, "Invalid credentials or you are not authorized.")
    
    return render(request, 'admin_login.html')



def admin_dashboard_view(request):
    return render(request,'admin_dashboard.html')

def user_dashboard(request):
    return render(request, 'f4fitness/user_dashboard.html')





def trainer_register_view(request):
    if request.method == 'POST':
        form = TrainerProfileForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Registration successful! Please login.')
            return redirect('trainer_managment')
        else:
            print(form.errors)  
    else:
        form = TrainerProfileForm()

    return render(request, 'f4fitness/trainer_register.html', {'form': form})




def trainer_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return render(request, 'trainer_login.html', {'login_success': True})
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('trainer_dashboard')  

    return render(request, 'f4fitness/trainer_login.html')


def trainer_dashboard_view(request):
    return render(request, 'f4fitness/trainer_dashboard.html')

def edit_trainer_details(request, trainer_id):
    trainer = get_object_or_404(TrainerProfile, id=trainer_id)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=trainer)
        if form.is_valid():
            form.save()  # Save updated data to the database
            return redirect('trainer_managment')  # Adjust redirect URL as needed
        else:
            print(form.errors)
            
    else:
        form = UserProfileForm(instance=trainer)

    return render(request, 'f4fitness/edit.html', {'form': form, 'trainer': trainer})


def delete_trainer(request,trainer_id):
    trainer=get_object_or_404(TrainerProfile,id=trainer_id)
    trainer.delete()
    return redirect('trainer_managment')










def user_management(request):
    users = UserProfile.objects.all() 
    return render(request, 'f4fitness/user_management.html', {'users': users})

def edit_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    else:
        form = UserForm(instance=user)
    return render(request, 'edit_user.html', {'form': form})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('user_management')
    return render(request, 'confirm_delete.html', {'user': user})












