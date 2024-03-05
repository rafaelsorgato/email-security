from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import change_profile_form,change_password_form
from django.http import HttpResponse,HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib import messages
from django.contrib.auth import authenticate, login,get_user
from django.contrib.auth.models import User


@login_required
def profile(request):
    user = request.user
    print(user.id)
    print(user.username)
    print(user.email)
    profile_form = change_profile_form()
    password_form = change_password_form()
    profile_form.fields['fullname'].widget.attrs['value'] = user.fullname
    profile_form.fields['fullname'].widget.attrs['value'] = user.username
    profile_form.fields['fullname'].widget.attrs['value'] = user.email
    
    return render(request, "profile.html",{'profile_form':profile_form,'password_form':password_form})



def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                messages.error(request, "User already exists")
            if form.cleaned_data['password'] != form.cleaned_data['repeatpassword']:
                messages.error(request, "Passwords doesn't match")
            if User.objects.filter(email=form.cleaned_data['email']).exists():
                messages.error(request, "Email already exists")
            if not User.objects.filter(username=form.cleaned_data['username']).exists() and form.cleaned_data['password'] == form.cleaned_data['repeatpassword']:
                User.objects.create_user(username=form.cleaned_data['username'],email=form.cleaned_data['email'],password=form.cleaned_data['password'])
                messages.error(request, "User created")
                return render(request, 'login.html', {'form': form})
            return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})

def user_login(request):
    form = LoginForm()
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username,password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/profile/')
            else:
                messages.error(request, "Wrong username/email or password")
                return render(request, 'login.html', {'form': form})
    return render(request, 'login.html', {'form': form})



