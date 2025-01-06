from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .forms import UserProfileForm
from .forms import TrainerProfileForm
from. import views
from.models import TrainerProfile
from django.shortcuts import get_object_or_404
from.models import UserProfile








def home(request):
    return render(request, "f4fitness/index.html")

def trainer_management(request):
    trainers = TrainerProfile.objects.all()
    return render(request, "trainer.html",{'trainers':trainers})



def register(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        if form.is_valid():
                form.save()  
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

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return render(request, 'login.html', {'login_success': True})
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('user_dashboard')  

    return render(request, 'f4fitness/login.html')





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












