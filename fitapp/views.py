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
from.models import plan
from .forms import PlanForm
from.models import Supplement
from .forms import SupplementForm
from.models import *










def home(request):
    return render(request, "f4fitness/index.html")

def trainer_management(request):
    trainers = TrainerProfile.objects.all()
    return render(request, "trainer.html",{'trainers':trainers})



def register(request,plan_id):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES)
        username=request.POST.get('username')
        password=request.POST.get('password')

        if form.is_valid():
                plan_obj=get_object_or_404(plan,id=plan_id)
                try:
                    user=User.objects.create_user(username=username,password=password)
                except Exception as e:
                    print(e)
                    render(request, 'f4fitness/register.html')
                profile=form.save(commit=False)
                profile.user=user
                profile.plan=plan_obj
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
    profile=UserProfile.objects.get(user=request.user)

    return render(request, 'f4fitness/user_dashboard.html',{'user_data':profile})





def trainer_register_view(request):
    if request.method == 'POST':
        form = TrainerProfileForm(request.POST, request.FILES)
        username=request.POST.get('username')
        password=request.POST.get('password')

        if form.is_valid():
            try:
                user=User.objects.create_user(username=username,password=password)
            except Exception as e:
                print(e)
                render(request, 'f4fitness/register.html')

            obj=form.save(commit=False)
            obj.user=user
            obj.save()
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
            return render(request, 'f4fitness/trainer_dashboard.html', {'login_success': True})
        else:
            messages.error(request, 'Invalid username or password')
            return redirect('trainer_login')  

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
    user = get_object_or_404(UserProfile, user__id=user_id)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_management')
    else:
        form = UserProfileForm(instance=user)
    return render(request, 'f4fitness/edit_user.html', {'form': form,'user_profile':user})

def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_management')










def plan_management(request):
    plans = plan.objects.all()
    return render(request, 'f4fitness/plan_management.html',{'plans':plans})


def addplans(request):
    from django.shortcuts import render, redirect
from .forms import PlanForm

def addplans(request):
    if request.method == 'POST':
        form = PlanForm(request.POST)
        if form.is_valid():
            form.save()
        
            return redirect('plan_management')  # Redirect to a success page after saving
        else:
            print(form.errors)
    form = PlanForm()

    return render(request, 'f4fitness/addplans.html', {'form': form})

    

def delete_plan(request, plan_id):
    plan_obj = get_object_or_404(plan, id=plan_id)
    plan_obj.delete()
    return redirect('plan_management')



def edit_plans(request, plan_id):
    plan_1 = get_object_or_404(plan, id=plan_id)
    print(plan_1)
    if request.method == 'POST':
        form = PlanForm(request.POST, instance=plan_1 )
        if form.is_valid():
            form.save()
            return redirect('plan_management')
    else:
        form = PlanForm(instance=plan_1)
    return render(request, 'f4fitness/edit_plans.html', {'plan': plan_1})





def userplan(request):
    uplan = plan.objects.all()
    return render(request, 'f4fitness/planview.html',{'plans':uplan})







def productmanagement(request):
    product = Supplement.objects.all()
    return render(request, 'f4fitness/productmanagement.html',{'product':product})

from django.shortcuts import render, redirect
from .forms import SupplementForm

def addsupplement(request):
    if request.method == 'POST':
        form = SupplementForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('productmanagement')  # Create a success page or redirect
    else:
        form = SupplementForm()
    return render(request, 'f4fitness/addsupplement.html', {'form': form})





def about(request):
    return render(request, 'f4fitness/about.html')



def payment_page(request):
    profile=UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        plan=profile.plan
        amount=plan.price
        upi=request.POST.get('upi')
        payment = Payment.objects.create( profile=profile, amount=amount,upi_id=upi)
        
        if payment:
            profile.paid=True
            profile.save()
        return render(request, 'f4fitness/success.html', {'payment': payment})
    return render(request, 'f4fitness/payment.html',{'plan':profile.plan})



def trainer_profile(request):
    profile = get_object_or_404(TrainerProfile, user=request.user)

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
        return redirect('trainer_profile')
    return render(request, 'trainer_profile.html', {'profile': profile})




def productview(request):
    product = Supplement.objects.all()
    return render(request, 'f4fitness/productview.html',{'product':product})






def edit_supplement(request, supplement_id):
    supplement_1 = get_object_or_404(Supplement, id=supplement_id)  # Fetch the specific supplement
    if request.method == "POST":
        form = SupplementForm(request.POST, request.FILES, instance=supplement_1)
        if form.is_valid():
            form.save()  # Save the updated supplement details
            return redirect('productmanagement')  # Redirect to the product management page
    else:
        form = SupplementForm(instance=supplement_1)  # Pre-fill form with existing data
    return render(request, 'f4fitness/edit_supplement.html', {'form': form, 'supplement': supplement_1})


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages  # For optional success messages
from .models import Supplement

def delete_supplement(request, supplement_id):
    supplement = get_object_or_404(Supplement, id=supplement_id)
    if request.method == "POST":
        supplement.delete()  # Delete the supplement
        messages.success(request, "Supplement deleted successfully.")  # Optional
        return redirect('productmanagement')  # Redirect to the product management page
    return render(request, 'f4fitness/confirm_delete_supplement.html', {'supplement': supplement})









from django.shortcuts import render, get_object_or_404, redirect
from .models import CustomerOrder
from django.http import HttpResponse

def product_list(request):
    products = Supplement.objects.all()
    return render(request, 'product_list.html', {'product': products})

def customer_form(request, product_id):
    product = get_object_or_404(Supplement, id=product_id)
    if request.method == "POST":
        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')
        upi_id = request.POST.get('upi_id')
        payment_mode = request.POST.get('payment_mode')
        
        CustomerOrder.objects.create(
            name=name,
            phone_number=phone_number,
            address=address,
            upi_id=upi_id,
            payment_mode=payment_mode,
            product=product,
            price=product.price
        )
        return HttpResponse("Order placed successfully!")

    return render(request, 'f4fitness/customer_form.html', {'product': product})







def order_success(request):
    return render(request, 'f4fitness/order_success.html',)







