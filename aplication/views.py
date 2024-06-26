from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import change_profile_form,change_password_form
from django.http import HttpResponse,HttpResponseRedirect
from .forms import LoginForm, RegisterForm,change_password_form,change_profile_form,Settings_forms
from django.contrib import messages
from django.contrib.auth import authenticate, login,get_user,logout
#from django.contrib.auth.models import User
from . import models
from .models import emails
from django.http import JsonResponse
import os
from django.conf import settings
from django.contrib.auth.hashers import check_password
import re
from bs4 import BeautifulSoup
from datetime import datetime
from django.db.models import Count
from django.db.models.functions import TruncMonth
from django.db.models.functions import ExtractMonth
import calendar
import json

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
            actualpassword = form.cleaned_data['actualpassword']
            if check_password(actualpassword, user.password):
                if password == repeatpassword:
                    if (len(password) < 8 or not re.search(r'[!@#$%^&*]', password) or not re.search(r'[A-Z]', password)):
                        messages.error(request,"New password didn't match all conditions")
                    else:
                        user.set_password(password)
                        try:
                            user.save()
                            messages.error(request,"Password Updated")
                        except:
                            messages.error(request,"Error while updating password, try again")   
                            return HttpResponseRedirect('/profile/')
                else:
                    messages.error(request,"Passwords didn't match")
                    return HttpResponseRedirect('/profile/')
            else:
                messages.error(request,"Wrong actual password")
                return HttpResponseRedirect('/profile/')

        if (form:=change_profile_form(request.POST, request.FILES)).is_valid():
            username = form.cleaned_data['username']
            user.fullname = form.cleaned_data['fullname']
            user.username = username
            user.email = form.cleaned_data['email'] 
            picture = None
            try: 
                picture = request.FILES['picture']
            except:
                pass
            if picture:
                if not picture.name.lower().endswith(('.jpg', '.jpeg', '.png', '.gif')):
                    messages.success(request,"File isn't an image")
                    return HttpResponseRedirect('/profile/')
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

def logout_user(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def dashboard(request):
    return render(request, 'dashboard.html')

def charts(request):
    # Obter o ano atual
    current_year = datetime.now().year

    # Lista de nomes abreviados dos meses
    month_abbr_names = [calendar.month_abbr[month_num] for month_num in range(1, 13)]

    # Inicializar os totais para todos os meses com zero
    monthly_totals = {month_abbr_names[i]: 0 for i in range(12)}
    # Consulta para obter o count de emails por mês do ano atual
    queueddata = emails.objects.filter(receivedondate__year=current_year) \
                        .annotate(month=ExtractMonth('receivedondate')) \
                        .values('month') \
                        .annotate(total=Count('id')) \
                        .order_by('month')
    queueddata_total_sum = sum(item['total'] for item in queueddata)
    noactiondata = emails.objects.filter(receivedondate__year=current_year, action=1) \
                        .annotate(month=ExtractMonth('receivedondate')) \
                        .values('month') \
                        .annotate(total=Count('id')) \
                        .order_by('month')
    quarantineddata = emails.objects.filter(receivedondate__year=current_year, action=2) \
                        .annotate(month=ExtractMonth('receivedondate')) \
                        .values('month') \
                        .annotate(total=Count('id')) \
                        .order_by('month')
    deleteddata = emails.objects.filter(receivedondate__year=current_year, action=3) \
                        .annotate(month=ExtractMonth('receivedondate')) \
                        .values('month') \
                        .annotate(total=Count('id')) \
                        .order_by('month')

    print(deleteddata)
    # Atualize os totais com os valores reais
    queueddata_total = monthly_totals.copy()
    noactiondata_total = monthly_totals.copy()
    deleteddata_total = monthly_totals.copy()
    quarantineddata_total = monthly_totals.copy()
    totaldata_total = monthly_totals.copy()
    for entry in noactiondata:
        # Ajuste o mês para corresponder aos índices da lista de meses abreviados
        month = month_abbr_names[entry['month'] - 1]
        total = entry['total']
        noactiondata_total[month] = total
    for entry in quarantineddata:
        # Ajuste o mês para corresponder aos índices da lista de meses abreviados
        month = month_abbr_names[entry['month'] - 1]
        total = entry['total']
        noactiondata_total[month] = total
    for entry in deleteddata:
        # Ajuste o mês para corresponder aos índices da lista de meses abreviados
        month = month_abbr_names[entry['month'] - 1]
        total = entry['total']
        deleteddata_total[month] = total
    for entry in queueddata:
        # Ajuste o mês para corresponder aos índices da lista de meses abreviados
        month = month_abbr_names[entry['month'] - 1]
        total = entry['total']
        queueddata_total[month] = total
    # Criar o contexto JSON
    print(month_abbr_names)
    for months in range(0,12):
        month = month_abbr_names[months]
        totaldata_total[month] = (deleteddata_total.get(month, 0) +
                          noactiondata_total.get(month, 0) +
                          noactiondata_total.get(month, 0)+
                          queueddata_total.get(month, 0))

    context = {
        'quarantineddata_total': list(quarantineddata_total.values()),
        'noactiondata_total': list(noactiondata_total.values()),
        'queueddata_total': queueddata_total_sum,
        'deleteddata_total': list(deleteddata_total.values()),
        'totaldata_total': list(totaldata_total.values()),
        'months': json.dumps(list(monthly_totals.keys())),
        'totals': list(monthly_totals.values())
    }


    # Converter para JSON
    json_context = json.dumps(context)

    print(json_context)
    return render(request, 'charts.html', context)

def tables(request):
    return render(request, 'tables.html')

def extract_text_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Remova todas as tags e obtenha apenas o texto
    tag = soup.find('body')
    text = tag.get_text()
    return text

def get_table_data(request):  
    actual_value = int(request.GET.get('valorAtual'))
    total_rows = emails.objects.all().count()
    emails_data = emails.objects.all().order_by('-receivedondate')[:actual_value]
    json_data = [{
        'id':email.id,
        'subject':email.subject,
        'sender':email.sender,
        'body':email.body,
        'receivedondate':email.receivedondate,
        'category':email.category,
        'action': "Queued" if email.action == 0 else "Pass" if email.action == 1 else "Junk" if email.action == 2 else "Quarantined" if email.action == 1 else None,
    } for email in emails_data]

    total_rows_json = {"total_rows": total_rows,"actual_value":actual_value}

    return JsonResponse({'table_data': json_data, 'total_rows_json': total_rows_json})

def get_htmlbody(request):
    # Obter o ID enviado pela requisição AJAX
    email_id = request.GET.get('id')
    print(email_id)
    # Filtrar os emails com base no ID
    try:
        email = emails.objects.get(id=email_id)
        html_body = email.htmlbody
    except emails.DoesNotExist:
        # Se o email com o ID especificado não for encontrado, retorne uma resposta vazia
        return JsonResponse({}, status=404)

    # Retornar o htmlbody do email encontrado
    return JsonResponse({'htmlbody': html_body})

    return JsonResponse(json_data, safe=False)

def rules(request):
    form = Settings_forms()
    return render(request, 'rules.html',{'form':form})
