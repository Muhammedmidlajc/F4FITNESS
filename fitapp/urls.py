from django.urls import path
from. import views



urlpatterns = [

  path('',views.home,name='home' ),

  # USER:-
  
  path('register/<int:plan_id>/', views.register, name='register'),

  path('login/', views.login_view, name='login'),

  path('user_dashboard/', views.user_dashboard, name='user_dashboard'),


 # ADMIN:-

  path('admin_login/', views.admin_login_view, name='admin_login'),

  path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),


  # TRAINER:-

  path('trainer_register/', views.trainer_register_view, name='trainer_register'),

  path('trainer_login/', views.trainer_login_view, name='trainer_login'),
  path('trainer_dashboard/', views.trainer_dashboard, name='trainer_dashboard'),
  path('trainer_plan/', views.trainer_plan, name='trainer_plan'),


  path('trainer_dashboard/', views.trainer_dashboard_view, name='trainer_dashboard'),
  path('trainer_managment/', views.trainer_management, name='trainer_managment'),
  path('edit_trainer_details/<int:trainer_id>/', views.edit_trainer_details, name='edit_trainer_details'),
  path('delete_trainer_details/<int:trainer_id>/', views.delete_trainer, name='delete_trainer'),

  path('logout/', views.logout_view, name='logout'),
  path('user_profile/', views.user_profile, name='user_profile'),
  path('user_progress/', views.user_progress, name='user_progress'),
  path('chatbot/', views.chatbot, name='chatbot'),



  path('productmanagement/', views.productmanagement, name='productmanagement'),
  path('add/', views.addsupplement, name='addsupplement'),
  path('edit/<int:supplement_id>/', views.edit_supplement, name='edit_supplement'),
  path('delete/<int:supplement_id>/', views.delete_supplement, name='delete_supplement'),

  




  path('users/', views.user_management, name='user_management'),
  path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
  path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
 
 
 

 
 path('plan_management/', views.plan_management, name='plan_management'),
 path('addplans/', views.addplans, name='addplans'),
 path('plan/delete/<int:plan_id>/', views.delete_plan, name='delete_plan'),
 path('plan/edit/<int:plan_id>/', views.edit_plans, name='edit_plans'),
 path('uplan/', views.userplan, name='uplan'),






  path('about/', views.about, name='about'),



  path('payment/', views.payment_page, name='payment_page'), 
  path('session_room/<int:session_id>/', views.session_room, name='session_room'), 
  path('save_session_progress/', views.save_session_progress, name='save_session_progress'), 
  path('session_status_update/<int:session_id>/', views.session_status_update, name='session_status_update'),
  path('user_workout/', views.user_workoutplan, name='user_workout'),





  path('productview/', views.productview, name='productview'),




  path('', views.product_list, name='product_list'),
  path('customer-form/<int:product_id>/', views.customer_form, name='customer_form'),


 path('customer-form/<int:product_id>/', views.customer_form, name='customer_form'),
 path('order-success/', views.order_success, name='order_success'), 
 path('trainer_profile/', views.trainer_profile, name='trainer_profile'), 
 path('manage_sessions/<int:plan_id>/', views.manage_sessions, name='manage_sessions'), 
 path('delete_sessions/<int:session_id>/', views.delete_session, name='delete_session'), 
 path('trainer_clients/',views.trainer_clients,name='trainer_clients'),
 path('user_products/', views.user_products, name='user_products'),

 path('cart/', views.cart_view, name='cart_view'),
 path('add_to_cart/', views.add_to_cart, name='add_to_cart'),
 path('product_payment/', views.product_payment, name='product_payment'),
 path('proceed_payment/', views.proceed_payment, name='proceed_payment'),
path('payment_success/', views.payment_success, name='payment_success'),
path('order_history/', views.order_history, name='order_history'),
path('diet_plan/', views.user_diet_plan, name='user_diet_plan'),
path('user_sessions/', views.user_sessions, name='user_sessions'),


path('trainer_diet_plan/<int:user_id>/', views.trainer_diet_plan, name='trainer_diet_plan'),
path('trainer_workoutplan/<int:user_id>/', views.trainer_workout_plan, name='trainer_workoutplan'),


path('add_diet_plan/<int:user_id>/', views.add_diet_plan, name='add_diet_plan'),
path('add_workout_plan/<int:user_id>/', views.add_workout_plan, name='add_workout_plan'),

path('delete_diet_plan/<int:plan_id>/', views.delete_diet_plan, name='delete_diet_plan'),
path('delete_workout_plan/<int:plan_id>/', views.delete_workout_plan, name='delete_workout_plan'),







]




