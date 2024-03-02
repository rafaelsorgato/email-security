from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .forms import change_profile_form,change_password_form

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

