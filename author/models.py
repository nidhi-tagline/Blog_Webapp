from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Author(models.Model):
    name = models.OneToOneField(User,on_delete=models.CASCADE)
    bio_detail = models.TextField()