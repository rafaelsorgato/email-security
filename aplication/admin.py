from django.contrib import admin
from .models import account,rule_settings
# Register your models here.

admin.site.register(account)

admin.site.register(rule_settings)
