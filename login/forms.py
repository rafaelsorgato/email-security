from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username or Email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}))

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class':'form-control', 'placeholder': 'Username'}))
    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'class':'form-control', 'placeholder': 'Email'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Password'}))
    repeatpassword = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class':'form-control', 'placeholder': 'Repeat Password'}))
