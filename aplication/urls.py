from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', views.profile , name='profile'),
    path('login/', views.user_login , name='login'),
    path('register/', views.register , name='register'),
    path('profile/', views.profile , name='profile'),
    path('logout/', views.logout_user, name='logout_user'),
] 

