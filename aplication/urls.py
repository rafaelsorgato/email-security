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
    path('dashboard/', views.dashboard, name='dashboard'),
    path('charts/', views.charts, name='charts'),
    path('tables/', views.tables, name='tables'),
    path('rules/', views.rules, name='rules'),
    path('get_table_data/', views.get_table_data, name='get_table_data'),
    path('get_htmlbody/', views.get_htmlbody, name='get_htmlbody'),


] 

