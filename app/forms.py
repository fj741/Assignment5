from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm, PasswordChangeForm
from django.utils.translation import gettext_lazy as _

class RegisterForm(UserCreationForm):
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    confirm_password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    class Meta:
        model = User
        fields = ['fname','lname', 'email', 'password', 'confirm_password']
    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')    
        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError('Passwords do not match')
        return confirm_password
    #Clean email function filters through the emails
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email has already been taken")
    def save(self, commit=True):
        user = super().save(commit=False)  
        user.set_password(self.cleaned_data('password'))  
        if commit:
            user.save()
        return user    
        
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['email', 'password']

class ProjectForm(forms.ModelForm):
    class Meta:
        model = Project
        fields = ['title', 'description']
        
#This form will allow an email to be sent for password reset        
class PasswordResetForm(PasswordResetForm):
    email = forms.EmailField(label = _("Email"), widget= forms.EmailInput())
    
class ResetPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['new_password1'].widget = forms.PasswordInput(attrs={'placeholder': 'New Password'})
        self.fields['new_password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})
        
    def save(self, commit=True):
        return super().save(commit)
            