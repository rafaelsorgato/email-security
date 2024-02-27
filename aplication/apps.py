from django.apps import AppConfig
import os



STATIC_DIR_APP1 = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/')


class AplicationConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'aplication'
