from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from django.contrib.auth.hashers import make_password, check_password
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User




# Create your views here.

def Register(request):
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
            if user:
                return HttpResponseRedirect('/profile/')
            else:
                messages.error(request, "Wrong username/email or password")
                return render(request, 'login.html', {'form': form})
    return render(request, 'login.html', {'form': form})


def profile(request):
    user_id = request.session.get('user_id')
    if user_id:
        messages.error(request, user_id)
        return render(request, 'login.html')
    else:
        return render('login')
    

