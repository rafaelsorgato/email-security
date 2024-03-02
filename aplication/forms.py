from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

user = get_user_model()
class change_profile_form(forms.Form):
    fullname = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Full Name', 'text' : '{{username}}'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}))
    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}))

class change_password_form(forms.Form):
    oldpassword = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control'}))
    repeatpassword = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control'}))
