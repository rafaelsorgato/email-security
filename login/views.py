from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import LoginForm, RegisterForm
from .models import users
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.contrib.auth import authenticate, login




# Create your views here.

def Register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] == form.cleaned_data['repeatpassword']:
                users.objects.create(username=form.cleaned_data['username'], password=make_password(form.cleaned_data['password']),email=form.cleaned_data['email'])
                return HttpResponseRedirect('/sucesso/')  # Redirecionar para a página de sucesso após o login
            else:
                messages.error(request, "Senhas não coincidem.")
                return render(request, 'register.html', {'form': form})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form': form})


def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, username=form.cleaned_data['username'], password=make_password(form.cleaned_data['password']))
            if user is not None:
                login(request, user)
                return HttpResponseRedirect('/seu-caminho-de-redirecionamento/')
            else:
                messages.error(request, "Wrong username or password")
                return render(request, 'login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})