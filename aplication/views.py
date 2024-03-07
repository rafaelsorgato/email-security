from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import change_profile_form,change_password_form
from django.http import HttpResponse,HttpResponseRedirect
from .forms import LoginForm, RegisterForm,change_password_form,change_profile_form
from django.contrib import messages
from django.contrib.auth import authenticate, login,get_user
#from django.contrib.auth.models import User
from . import models
from django.http import JsonResponse
import os
from django.conf import settings

User = models.account

@login_required
def profile(request):
    user = request.user
    if request.method == "POST":
        password = user.password
        username = user.username
        if (form:=change_password_form(request.POST)).is_valid():
            password = form.cleaned_data['password']
            repeatpassword = form.cleaned_data['repeatpassword']
            oldpassword = form.cleaned_data['oldpassword']
            user.set_password(password)
            try:
                user.save()
                messages.error(request,"Password Updated")
            except Exception as e:
                messages.error(request,"Passwords didn't match")
        if (form:=change_profile_form(request.POST, request.FILES)).is_valid():
            username = form.cleaned_data['username']
            user.fullname = form.cleaned_data['fullname']
            user.username = username
            user.email = form.cleaned_data['email']  
            picture = request.FILES['picture']
            print(picture)
            user.picture = '/static/img_uploads/' + picture.name
            with open('aplication/static/img_uploads/' + picture.name, 'wb+') as destination:
                    for chunk in picture.chunks():
                        destination.write(chunk)
            try:
                user.save()
                messages.success(request,"Profile Updated")
            except Exception as e:
                messages.success(request,"USERNAME OR EMAIL ALREADY EXISTS")
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request, user)  
        return HttpResponseRedirect('/profile/')
    elif request.method == 'GET':   
        profile_form = change_profile_form()
        password_form = change_password_form()
        profile_form.fields['fullname'].widget.attrs['value'] = user.fullname
        profile_form.fields['username'].widget.attrs['value'] = user.username
        profile_form.fields['email'].widget.attrs['value'] = user.email

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
                User.objects.create_user(username=form.cleaned_data['username'],fullname=form.cleaned_data['fullname'],email=form.cleaned_data['email'],password=form.cleaned_data['password'])
                messages.success(request, "User created")
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
