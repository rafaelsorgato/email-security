from django import forms

class loginform(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(attrs={'class': 'password-toggle'}))
