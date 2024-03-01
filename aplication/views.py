from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import change_profile_form,change_password_form

@login_required
def profile(request):
    profile_form = change_profile_form()
    password_form = change_password_form()
    return render(request, "profile.html",{'profile_form':profile_form,'password_form':password_form})