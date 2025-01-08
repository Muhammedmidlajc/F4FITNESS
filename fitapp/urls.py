from django.urls import path
from. import views



urlpatterns = [

  path('',views.home,name='home' ),

  # USER:-
  
  path('register/', views.register, name='register'),

  path('login/', views.login_view, name='login'),

  path('user_dashboard/', views.user_dashboard, name='user_dashboard'),


 # ADMIN:-

  path('admin_login/', views.admin_login_view, name='admin_login'),

  path('admin_dashboard/', views.admin_dashboard_view, name='admin_dashboard'),


  # TRAINER:-

  path('trainer_register/', views.trainer_register_view, name='trainer_register'),

  path('trainer_login/', views.trainer_login_view, name='trainer_login'),

  path('trainer_dashboard/', views.trainer_dashboard_view, name='trainer_dashboard'),
  path('trainer_managment/', views.trainer_management, name='trainer_managment'),
  path('edit_trainer_details/<int:trainer_id>/', views.edit_trainer_details, name='edit_trainer_details'),
  path('delete_trainer_details/<int:trainer_id>/', views.delete_trainer, name='delete_trainer'),

  path('logout/', views.logout_view, name='logout'),
  path('user_profile/', views.user_profile, name='user_profile'),
  path('user_progress/', views.user_progress, name='user_progress'),
  path('chatbot/', views.chatbot, name='chatbot'),


  
 






  path('users/', views.user_management, name='user_management'),
  path('users/edit/<int:user_id>/', views.edit_user, name='edit_user'),
  path('users/delete/<int:user_id>/', views.delete_user, name='delete_user'),
 
 
 




]