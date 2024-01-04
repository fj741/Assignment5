from django.shortcuts import render, redirect, get_object_or_404 
from .models import *
from django.contrib.auth import login, authenticate, logout
from .forms import RegisterForm, LoginForm, PasswordResetForm, ProjectForm
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required

@login_required(login_url="login")
def home(request):
    fname = request.user.fname
    return render(request, 'main/home.html')

def logout(request):
    logout(request)
    return redirect('login')

def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'users/register.html', {'form': form})           

    
def login(request):
    if request.method == "POST":
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data('email')
            password = form.cleaned_data('password')
            user = authenticate(request, email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                return redirect('register')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form':form})    

#This function is used to create a project 
@login_required(login_url="login")
def create_project(request):
    if request.method == "POST":
        form = ProjectForm()
        if form.is_valid():
            project = form.save(commit=False)
            project.save()
    else:
        form = ProjectForm()
    return render(request, "main/create_project.html",{"form": form})

#I created two views which will edit or delete a specific project created. 
#Each of these functions uses the get_object_or_404 to take the id of the particular project. 
#If the id doesn't exist, it returns a 404 message 
#Once again the user must be signed in to use any of these functions.

@login_required(login_url="login")
def edit_project(request, project_id):
    project = get_object_or_404(Project, project_id)
    if request.mthod == "POST":
        form = ProjectForm(request.POST, instance=project)
        if form.is_valid():
            form.save()
            return redirect('home', project_id = project_id)
    else:
        form = ProjectForm(instance = project)
    return render(request, "main/edit_project.html", {"form": form})    

@login_required(login_url="login")
def delete_project(request, project_id):
    project = get_object_or_404(Project, project_id)
    
    if request.method == "POST":
        project.delete()
        return redirect("home")
class password_reset_email_view(auth_views.PasswordResetView):
    form = PasswordResetForm
    template = 'users/reset_password.html'