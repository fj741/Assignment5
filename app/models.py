from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager  ,PermissionsMixin
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class UserManager(BaseUserManager):
    def create(self, email, fname, lname, password=None, **extra_fields):
        if not email:
            raise ValueError("Please enter a valid email")
        
        email = self.normalize_email(email)
        user = self.model(email=email, fname=fname, lname=lname)
        user.set_password(password)
        user.save(using=self._db)
        return user
        
    def create_superuser(self, email, password=None, **extra_fields):
            extra_fields.setdefault("is_staff", True)
            extra_fields.setdefault("is_superuser", True)
            
            if extra_fields.get('is_staff') is not True:
                raise ValueError("Superuser must have staff = True")
            
            if extra_fields.get('is_superuser') is not True:
                raise ValueError("Superuser must be true")
            return self.create(email, password, **extra_fields)
            
        
class User(AbstractBaseUser, PermissionsMixin):
    fname = models.CharField(verbose_name="First Name",  max_length=50)        
    lname = models.CharField(verbose_name="Last Name",  max_length=50)
    email = models.EmailField(verbose_name="Email",unique=True)
    date_joined = models.DateTimeField(_('date_joined'), default=timezone.now)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager() 
     
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['fname', 'lname']
    
    
    def first_name(self):
        return self.fname
    
    def full_name(self):
        return f"{self.fname} {self.lname}"
    
    def __str__(self):
        return self.email
    
    
class Project(models.Model):
    title = models.CharField(max_length=50)
    owner = models.ForeignKey(User, on_delete= models.CASCADE)
    description = models.TextField(default="No description has been added")
    created = models.DateTimeField(default=timezone.now())
    
    def __str__(self):
        return self.title
