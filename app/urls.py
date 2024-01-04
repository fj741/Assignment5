from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login" ),
    path('logout/', views.logout, name="logout"),
    
    path('create_project/', views.create_project, name="create_project"),
    #The following url gives the link to edit a specific project using the project id
    path('edit_project/<int:project_id>', views.edit_project, name="edit_project"),
    
    #Django has built in views for password reset. However, I created my own templates for password reset
    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='users/reset_password.html'), name="reset_password"),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='users/email_sent.html'), name="password_reset_done"),
    #The following path will encode the users id and a base 64 encription
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='users/create_new_password.html'), name="password_reset_confirm"),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='users/new_password_confirmed.html'), name="password_reset_complete")
]
