from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate

# Create your models here.
class account(AbstractUser):
    STATUS_CHOICES = (
        ('user', 'User'),
        ('admin', 'Admin'),
        ('custom', 'Custom'),
    )
        
    fullname = models.TextField(max_length=100)
    username = models.TextField(max_length=100, unique=True)
    email = models.TextField(max_length=100, unique=True)
    password = models.TextField(max_length=100)
    picture = models.ImageField(upload_to='aplication/static/img_uploads', blank=True, null=True)
    status = models.TextField(default = 'user', choices=STATUS_CHOICES)

    def __str__(self):
        return self.username
    
    @staticmethod
    def authenticate_user(username, password):
        return authenticate(username=username, password=password)