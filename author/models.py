from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self,username,password=None,**extra_fields):
        user = self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, username, password= None, **extra_fields):
        user = self.create_user(username=username, password=password, **extra_fields)
        user.is_admin = True
        user.save()
        return user

class Author(AbstractBaseUser):
    username = models.CharField(max_length=50,unique=True)
    bio_detail = models.TextField()
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    def __str__(self):
        return self.username
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin