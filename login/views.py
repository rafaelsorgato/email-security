from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .forms import LoginForm
# Create your views here.

def login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            # Lógica de autenticação aqui
            return HttpResponseRedirect('/sucesso/')  # Redirecionar para a página de sucesso após o login
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})


