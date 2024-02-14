from django.shortcuts import render
from django.http import HttpResponse
from .forms import loginform
# Create your views here.

def login(request):
    return render(request,"login.html",context={"loginform": loginform}) 


#from home.forms import loginform
# Create your views here.

#def home(request):
#    loginformpage = loginform
#    context = {"loginform": loginformpage}  # Adicione todas as variáveis de contexto aqui