from django import forms
from django.contrib.auth import authenticate, login
from django.contrib.auth import get_user_model

user = get_user_model()
class change_profile_form(forms.Form):
    fullname = forms.CharField(max_length=100,widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Full Name', 'id':"fullname"}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username', 'id':"username"}))
    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email', 'id':"email"}))
    picture = forms.FileField(widget=forms.FileInput(attrs={'class': "btn btn-primary", 'id': "picture", 'accept': 'image/*','style': 'display:none;'} ),required=False)

class change_password_form(forms.Form):
    actualpassword = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control', 'id':"actualpassword"}))
    password = forms.CharField(max_length=100,widget=forms.PasswordInput(attrs={'class':'form-control', 'id':"password","placeholder":"Must have at least 8 chars (At least 1 big letter, 1 number and 1 special char)"}))
    repeatpassword = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'id':"repeatpassword"}))


class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Username or Email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Password'}))

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Username'}))
    fullname= forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Fullname'}))
    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Password'}))
    repeatpassword = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control form-control-user', 'placeholder': 'Repeat Password'}))



settings_choices = [
    ("low", "Low"),
    ("medium", "Medium"),
    ("aggressive", "Aggressive")
]

class Settings_forms(forms.Form):
    antispam = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control form-control-user'}), choices=settings_choices)
    antiphishing = forms.ChoiceField(widget=forms.Select(attrs={'class': 'form-control form-control-user'}), choices=settings_choices)
