from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import authenticate
from django.db.models.signals import post_migrate
from django.dispatch import receiver

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
    picture = models.ImageField(upload_to='static/img_uploads', blank=True, null=True, default="../static/img_uploads/default.png")
    status = models.TextField(default = 'user', choices=STATUS_CHOICES)

    def __str__(self):
        return self.username
    
    @staticmethod
    def authenticate_user(username, password):
        return authenticate(username=username, password=password)
    
class rule_settings(models.Model):
    SETTINGS_CHOICES = (
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('agressive', 'Agressive'),
    )

    antispam = models.CharField(default = 'low', choices=SETTINGS_CHOICES, max_length=20)
    antiphishing = models.CharField(default = 'low', choices=SETTINGS_CHOICES, max_length=20)

@receiver(post_migrate)
def create_default_rule_settings(sender, **kwargs):
    if sender.name == 'aplication':  # substitua 'your_app' pelo nome do seu aplicativo
        rule_settings.objects.get_or_create(antispam='low', antiphishing='low')
        

class emails(models.Model):

    subject = models.CharField(max_length=100)
    sender = models.CharField(max_length=100)
    htmlbody = models.CharField(max_length=100)
    body = models.CharField(max_length=100)
    receivedondate = models.DateTimeField()
    action = models.IntegerField(
            default=0
        )
    category = models.CharField(
            default="Queued",max_length=100
        )
