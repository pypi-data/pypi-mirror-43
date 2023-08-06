from django.apps import AppConfig
from django.contrib.auth.models import User
from django.conf import settings
from .core import DjangoAutoUser


class DjangoAutoUserConfig(AppConfig):
    name = 'autouser'
    verbose_name = "Django Auto User"
    def ready(self):
        DjangoAutoUser()
    

