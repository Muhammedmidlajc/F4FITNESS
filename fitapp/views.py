from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import UserProfileForm
from .forms import TrainerProfileForm
from.models import TrainerProfile
from django.shortcuts import get_object_or_404
from.models import UserProfile
from django.contrib.auth.models import User
from.models import plan
from .forms import PlanForm
from.models import Supplement,Attendance
from .forms import SupplementForm
from.models import *
from .models import Session
from django.contrib.auth.decorators import login_required
from datetime import timedelta





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
                print(plan_obj,'fffff')
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

def admin_login(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(username=username,password=password)
        if user and user.is_superuser == True:
            return redirect('admin_dashboard')
    return render(request,'admin_login.html')


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
    return redirect('home')

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
import google.generativeai as genai


GOOGLE_API_KEY='AIzaSyACYwJ4-I9RZgK7eoZhWRKKFmuaFII6xCw'

def get_answer(question):

    prompt = f"""
    Please analyze the following text and answer the question.
    
    Question: {question}
    
    text: {BotData.objects.filter().first().content}
    
    Please provide a clear and concise answer based on the document content above.
    only need answer do not reflect questions

    also response like gym bot if talk casually like hii ,heloo 
    """
    
    # Using Gemini
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
    try:
        response = model.generate_content(prompt)
        answer = response.text.strip()
        return {'response': answer}

    except Exception as e:
        print(e)
        return False



def chatbot(request):
    if request.method == 'POST':
        data = json.loads(request.body) 
        user_message = data.get('message') 

        res=get_answer(user_message)
        if not res == False:
            return JsonResponse(res)
        else:
            return JsonResponse({'response': 'your bot is not available now '})

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
    today=datetime.datetime.today()
    
    if Attendance.objects.filter(user=profile,date=today).exists():
        att_status=True
    else:
        att_status=False
    return render(request, 'f4fitness/user_dashboard.html',{'user_data':profile,'att_status':att_status})





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


def trainer_dashboard(request):
    users=UserProfile.objects.filter(trainer=request.user.trainerprofile)
    user_count=users.count()
    session_count=Session.objects.all().count()
    date=datetime.date.today()
    if trainer_Attendance.objects.filter(trainer=request.user.trainerprofile ,date=date).exists():
        att_status=True
    else:
        att_status=False
    return render(request,'f4fitness/trainer_dashboard.html',{'user_count':user_count,'session_count':session_count,'att_status':att_status})


def trainer_plan(request):
    plans = plan.objects.all()
    return render(request, 'trainer_plan.html', {'plans': plans})


def trainer_login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful!')
            return redirect('trainer_dashboard')
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
    users = UserProfile.objects.filter(plan__Type="Online") 
    trainers=TrainerProfile.objects.all()
    return render(request, 'f4fitness/user_management.html', {'users': users,'trainers':trainers})


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


import datetime
def payment_page(request):
    profile=UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        plan=profile.plan
        amount=plan.price
        upi=request.POST.get('upi')
        payment = Payment.objects.create( profile=profile, amount=amount,upi_id=upi)
        print(payment)
        
        if payment:
            sessions = Session.objects.filter(plan=plan).order_by('order')
            for session in sessions:
                UserSession.objects.create(session=session, user=profile, date_completed=datetime.datetime.now(), order=session.order)

            profile.paid = True
            profile.payment_date=datetime.date.today()
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


def manage_sessions(request, plan_id):
    sessions = Session.objects.filter(plan__id=plan_id).order_by('order')
    if request.method == 'POST':
        time = request.POST.get('time')
        duration = request.POST.get('duration')
        title = request.POST.get('title')
        order = request.POST.get('order')
        trainer = request.user.trainerprofile 
        video=request.FILES.get('video')
        new_session = Session(plan_id=plan_id,video=video,order=order,title=title ,time=time, duration=duration, trainer=trainer)
        new_session.save()
        messages.success(request, 'Session added successfully!')
        return redirect('manage_sessions', plan_id=plan_id)
    return render(request, 'sessions.html', {'sessions': sessions, 'plan_id': plan_id})


def delete_session(request, session_id):
    session = get_object_or_404(Session, id=session_id)
    session.delete() 
    messages.success(request, "Session deleted successfully.")  
    return redirect('manage_sessions', plan_id=session.plan.id) 

@login_required(login_url='/login/')
def user_products(request):
    products = Supplement.objects.all()
    return render(request, 'user_products.html', {'supplements': products})


def cart_view(request):
    cart_items = request.session.get('cart_items', [])
    total_price = sum(float(item['price']) * item['quantity'] for item in cart_items)
    return render(request, 'cart.html', {'cart_items': cart_items, 'total_price': total_price})


def add_to_cart(request):
    item_id = request.GET.get('item_id', None)
    decrease = request.GET.get('decrease', False)
    remove = request.GET.get('remove', False)
    if item_id:
        product = get_object_or_404(Supplement, id=item_id)
        cart_items = request.session.get('cart_items', [])
        
        product_price = float(product.price)
        image = product.image.url
        
        existing_item = next((item for item in cart_items if item['id'] == product.id), None)
        if remove: 
            if existing_item:
                cart_items.remove(existing_item)  
                messages.success(request, f'{product.name} has been removed from your cart.')
        elif existing_item:
            if decrease: 
                existing_item['quantity'] -= 1
                if existing_item['quantity'] <= 0:
                    cart_items.remove(existing_item)
            else:
                existing_item['quantity'] += 1
        else:
            cart_item = {
                'id': product.id,
                'name': product.name,
                'price': product_price, 
                'quantity': 1,
                'image':image
            }
            cart_items.append(cart_item)
        
        request.session['cart_items'] = cart_items
        if not decrease and not remove:
            messages.success(request, f'{product.name} has been added to your cart.')
    return redirect('cart_view')

def product_payment(request):
    cart_items = request.session.get('cart_items', [])
    total_price = sum(float(item['price']) * item['quantity'] for item in cart_items)
    return render(request, 'product_payment.html', {'cart_items': cart_items, 'total_price': total_price})


def proceed_payment(request):
    if request.method == "POST":
        cart_items = request.session.get('cart_items', [])
        user = get_object_or_404(UserProfile, user=request.user)
        total_price = sum(float(item['price']) * item['quantity'] for item in cart_items)
        quantity_list = []

        for item in cart_items:
            product = get_object_or_404(Supplement, id=item['id'])
            obj = ProductWithQuantity.objects.create(supplement=product, quantity=item['quantity'])
            quantity_list.append(obj)

        payment_method = request.POST.get('payment_method')
        if payment_method == 'card':
            card_number = request.POST.get('card_number')
            expiry_date = request.POST.get('expiry_date')
            cvv = request.POST.get('cvv')
            cardholder_name = request.POST.get('cardholder_name')
            payment = BuyHistory.objects.create(user=user, total_amount=total_price,card_number=card_number,expiry_date=expiry_date,cardholder_name=cardholder_name,cvv=cvv,payment_method='card')
        
        elif payment_method == 'upi':
            upi_id = request.POST.get('upi_id')
            payment = BuyHistory.objects.create(user=user, total_amount=total_price,upi_id=upi_id,payment_method='upi')

        payment.supplements.add(*quantity_list)
        request.session['cart_items'] = [] 
        messages.success(request, "Your cart has been cleared.")
        return redirect('payment_success')
    
    return redirect('product_payment')


def payment_success(request):
    cart_items = request.session.get('cart_items', [])
    total_price = sum(float(item['price']) * item['quantity'] for item in cart_items)
    return render(request, 'payment_success.html', {'cart_items': cart_items, 'total_price': total_price})

def order_history(request):
    user = get_object_or_404(UserProfile, user=request.user)
    purchase_history = BuyHistory.objects.filter(user=user).order_by('-purchase_date')
    return render(request, 'orders.html', {'purchase_history': purchase_history})

def user_diet_plan(request):
    user = get_object_or_404(UserProfile, user=request.user)
    diet_plan = DietPlan.objects.filter(user=user)
    return render(request, 'user_diet_plan.html', {'diet_plan': diet_plan})


def trainer_clients(request):
    clients=UserProfile.objects.filter(trainer=request.user.trainerprofile)
    return render(request,'trainer_clients.html',{'clients':clients})


def user_sessions(request):
    user = get_object_or_404(UserProfile, user=request.user)
    all_sessions=UserSession.objects.filter(user=user)
    upcoming_sessions = all_sessions.filter(status='upcoming')
    completed_sessions = all_sessions.filter(status='completed')

    for session in upcoming_sessions:
        session.unlocked = False  
        if session.order == 1:
            session.unlocked = True 
        elif completed_sessions:
            latest_completed=completed_sessions.order_by('order').first()
            previous_session = all_sessions.filter(order=session.order - latest_completed.order).first()
            if previous_session and previous_session.status == 'completed':
                session.unlocked = True  

    return render(request, 'upcoming_classes.html', {'upcoming_sessions': upcoming_sessions, 'completed_sessions': completed_sessions})


def session_room(request,session_id):
    user_session=get_object_or_404(UserSession,id=session_id)
    try:
        session_progress=SessionProgress.objects.get(user_session=user_session)
        prev_duration=session_progress.duration
    except:
        prev_duration=0

    return render(request,'goto_session.html',{'session':user_session,'prev_duration':prev_duration,'status':user_session.status})


def save_session_progress(request):
    if request.method == 'POST':

        data = json.loads(request.body)
        session_id = data.get('sessionId')
        time_spent = data.get('timeSpent')

        session,_=SessionProgress.objects.get_or_create(user_session_id=session_id)
        session.duration=time_spent
        session.save()

        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)


def session_status_update(request,session_id):
    user_session=get_object_or_404(UserSession,id=session_id)
    user_session.status='completed'
    user_session.save()
    return redirect ('session_room',session_id=session_id)



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


def user_workoutplan(request):
    user_profile = get_object_or_404(UserProfile, user=request.user)
    workout_plans = WorkoutPlan.objects.filter(user=user_profile)
    return render(request, 'user_workout.html', {'workout_plans': workout_plans})


def trainer_diet_plan(request,user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    diet_plans = DietPlan.objects.filter(user=user_profile)
    return render(request, 'trainer_diet_plan.html', {'diet_plans': diet_plans,'user_id':user_id})

def trainer_workout_plan(request,user_id):
    user_profile = get_object_or_404(UserProfile, id=user_id)
    workout_plans = WorkoutPlan.objects.filter(user=user_profile)
    return render(request, 'trainer_workout_plan.html', {'workout_plans': workout_plans,'user_id':user_id})



def add_workout_plan(request,user_id):
    if request.method == "POST":
        exercise_name = request.POST.get('exercise_name')
        duration = request.POST.get('duration')
        sets = request.POST.get('sets')
        repetitions = request.POST.get('repetitions')
        notes = request.POST.get('notes')
        user_profile = get_object_or_404(UserProfile,id=user_id)

        WorkoutPlan.objects.create(
            user=user_profile,
            exercise_name=exercise_name,
            duration=duration,
            sets=sets,
            repetitions=repetitions,
            notes=notes
        )
        return redirect('trainer_workoutplan', user_id=user_id)

    return render(request, 'add_workout_plan.html',{'user_id':user_id})

def add_diet_plan(request,user_id):
    if request.method == "POST":
        breakfast = request.POST.get('breakfast')
        lunch = request.POST.get('lunch')
        dinner = request.POST.get('dinner')
        snacks = request.POST.get('snacks')
        user_profile = get_object_or_404(UserProfile,id=user_id)

        DietPlan.objects.create(
            user=user_profile,
            breakfast=breakfast,
            lunch=lunch,
            dinner=dinner,
            snacks=snacks
        )
        return redirect('trainer_diet_plan',user_id=user_id)

    return render(request, 'add_diet_plan.html',{'user_id':user_id})


def delete_diet_plan(request, plan_id):
    diet_plan = get_object_or_404(DietPlan, id=plan_id)
    diet_plan.delete()
    return redirect('trainer_diet_plan', user_id=diet_plan.user.id)


def delete_workout_plan(request, plan_id):
    workout_plan = get_object_or_404(WorkoutPlan, id=plan_id)
    workout_plan.delete()
    return redirect('trainer_workoutplan', user_id=workout_plan.user.id)


def my_attendance(request):
    today=datetime.date.today()
    user_profile = request.user.userprofile
    start_date = user_profile.payment_date if user_profile.payment_date else  today.replace(day=1)
    date_range = []
    current_date = start_date
    while current_date <= today:
        date_range.append(current_date)
        current_date += timedelta(days=1)
    
    attendances = Attendance.objects.filter(
        user=user_profile,
        date__gte=start_date,
        date__lte=today
    ).values_list('date', flat=True)
    
    present_dates = set(attendances)
    attendance_status = [
        {
            'date': single_date,
            'status': 'present' if single_date in present_dates else 'absent'
        }
        for single_date in date_range
    ]
    return render(request, 'my_attendance.html', {'attendance_status': attendance_status})


def offline_usermanagement(request):
    users = UserProfile.objects.filter(plan__Type="Offline") 
    trainers=TrainerProfile.objects.all()
    return render(request, 'f4fitness/offline_usermangement.html', {'users': users,'trainers':trainers})


def mark_attendance(request):  
    today=datetime.datetime.today()
    user=get_object_or_404(UserProfile,user=request.user)
    if Attendance.objects.filter(user=user,date=today).exists():
        return redirect('user_dashboard')
    attendence=Attendance.objects.create(user=user,date=today,status=True)
    return redirect('user_dashboard')


def assign_trainer(request,user_id):
    if request.method == 'POST':
        user=get_object_or_404(UserProfile,id=user_id)
        trainer_id=request.POST.get('trainer')
        trainer=get_object_or_404(TrainerProfile,id=trainer_id)
        user.trainer=trainer    
        user.save()
    return redirect('user_management')



def trainer_mark_attendance(request):  
    today=datetime.datetime.today()
    trainer=get_object_or_404(TrainerProfile,user=request.user)
    if trainer_Attendance.objects.filter(trainer=trainer,date=today).exists():
        return redirect('trainer_dashboard')
    attendence=trainer_Attendance.objects.create(trainer=trainer,date=today,status=True)
    return redirect('trainer_dashboard')



def trainer_attendance(request):
    today=datetime.date.today()
    trainer_profile = request.user.trainerprofile
   
    start_date = today.replace(day=1)
    date_range = []
    current_date = start_date
    while current_date <= today:
        date_range.append(current_date)
        current_date += timedelta(days=1)
    
    attendances = trainer_Attendance.objects.filter(
        trainer=trainer_profile,
        date__gte=start_date,
        date__lte=today
    ).values_list('date', flat=True)
    
    print(attendances,'asdfafd')
    present_dates = set(attendances)
    attendance_status = [
        {
            'date': single_date,
            'status': 'present' if single_date in present_dates else 'absent'
        }
        for single_date in date_range
    ]
    print(attendance_status)
    return render(request, 'f4fitness/trainer_attendance.html', {'attendance_status': attendance_status})



import cv2
import face_recognition
from django.views import View
from django.http import JsonResponse
import base64
import json,os
import numpy as np

class CameraFaceRecognitionView(View):
    def __init__(self):
        self.known_faces = []
        users=UserProfile.objects.all()
        for user in users:
            if user.image:
                image_path = user.image.path  
                if os.path.exists(image_path):
                    img = face_recognition.load_image_file(image_path)
                    encodings = face_recognition.face_encodings(img)
                    if encodings:
                        self.known_faces.append({
                            "name": user.name,
                            "image_path": user.image.url, 
                            "encoding": encodings[0] 
                        })
                    else:
                        print(f"⚠️ No face found in {user.name}'s image: {image_path}")

        print(self.known_faces)
    def get(self, request):
        return render(request, 'faces.html')

    def post(self, request):
        try:
            data = json.loads(request.body)
            image_data = data.get('image')

            if ',' in image_data:
                image_data = image_data.split(',')[1]

            nparr = np.frombuffer(base64.b64decode(image_data), np.uint8)
            img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

            if img is None:
                return JsonResponse({'status': 'error', 'message': 'Invalid image data'})

            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

            face_locations = face_recognition.face_locations(img_rgb, model="hog")

            if not face_locations:
                return JsonResponse({'status': 'success', 'faces': []})

            face_encodings = face_recognition.face_encodings(img_rgb, face_locations)

            faces_info = []
            for i, (top, right, bottom, left) in enumerate(face_locations):
                match_found = False
                matched_user = None

                if i < len(face_encodings):
                    for user in self.known_faces:
                        match = face_recognition.compare_faces([user["encoding"]], face_encodings[i])[0]
                        if match:
                            match_found = True
                            matched_user = user
                            break  # Stop checking after the first match

                face_info = {
                    'x': left,
                    'y': top,
                    'width': right - left,
                    'height': bottom - top,
                    'match': match_found,
                    'matched_user': {
                        "name": matched_user["name"],
                        "image_path": matched_user["image_path"]
                    } if match_found else None
                }
                faces_info.append(face_info)

            return JsonResponse({'status': 'success', 'faces': faces_info})

        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})








def view_attendance(request, user_id):
    user = get_object_or_404(UserProfile, id=user_id)
    attendance_records = Attendance.objects.filter(user=user)
    return render(request, 'f4fitness/view_attendance.html', {'user': user, 'attendance_records': attendance_records})





from django.db.models import Q
def chat(request):
    trainer=get_object_or_404(UserProfile,user=request.user).trainer
    trainer_id=trainer.user.id if trainer else None
    messages = ChatMessage.objects.filter(
    Q(sender=request.user, receiver=trainer.user) | 
    Q(sender=trainer.user, receiver=request.user)
    ).order_by('timestamp')
    return render(request, 'f4fitness/chat.html',{'trainer_id':trainer_id,'messages':messages})


def trainer_chat(request):
    trainer=get_object_or_404(TrainerProfile,user=request.user)
    user_id=request.GET.get('user_id')
    messages = ChatMessage.objects.filter(
    (Q(sender__id=user_id, receiver=trainer.user) | Q(sender=trainer.user, receiver__id=user_id))
    ).order_by('timestamp')

    return render(request, 'trainer_chat.html',{'user_id':user_id,'messages':messages})


def send_message(request):
    if request.method == 'POST':
        trainer_id=request.GET.get('trainer_id')
        message = request.POST.get('message', '')
        if trainer_id:
            trainer=get_object_or_404(User,id=trainer_id)
            ChatMessage.objects.create(sender=request.user, receiver=trainer, message=message)
        return redirect('chat')


from django.urls import reverse
def send_message_trainer(request):
    if request.method == 'POST':
        trainer_id = request.GET.get('trainer_id')
        user_id = request.GET.get('user_id')
        message = request.POST.get('message', '')

        if trainer_id:
            trainer = get_object_or_404(User, id=trainer_id)
            ChatMessage.objects.create(sender=request.user, receiver=trainer, message=message)
        return redirect(f"{reverse('trainer_chat')}?user_id={user_id}") 



from django.db.models import OuterRef, Subquery
def user_chatlist(request):
    latest_messages = ChatMessage.objects.filter(
        receiver=request.user,
        sender=OuterRef('sender')
    ).order_by('-timestamp').values('timestamp')[:1]

    chats = ChatMessage.objects.filter(
        receiver=request.user,
        timestamp=Subquery(latest_messages)
    ).order_by('-timestamp')

    return render(request, 'f4fitness/user_chatlist.html', {'chats': chats})






