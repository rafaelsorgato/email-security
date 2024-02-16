from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'u-border-2 u-border-grey-10 u-grey-10 u-input u-input-rectangle u-block-3eea-9', 'placeholder': 'Enter your Username'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'u-border-2 u-border-grey-10 u-grey-10 u-input u-input-rectangle u-block-3eea-12', 'placeholder': 'Enter your Password'}))

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'class': 'u-border-2 u-border-grey-10 u-grey-10 u-input u-input-rectangle u-block-3eea-9', 'placeholder': 'Enter your Username'}))
    email = forms.CharField(max_length=100, widget=forms.EmailInput(attrs={'class': 'u-border-2 u-border-grey-10 u-grey-10 u-input u-input-rectangle u-block-3eea-9', 'placeholder': 'Enter your Username'}))
    password = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'u-border-2 u-border-grey-10 u-grey-10 u-input u-input-rectangle u-block-3eea-12', 'placeholder': 'Enter your Password'}))
    repeatpassword = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'u-border-2 u-border-grey-10 u-grey-10 u-input u-input-rectangle u-block-3eea-12', 'placeholder': 'Enter your Password'}))
