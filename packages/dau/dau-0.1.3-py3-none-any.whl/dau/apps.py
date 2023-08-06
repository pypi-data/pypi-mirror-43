from django.apps import AppConfig
from django.db.models import signals
from django.apps import apps
from . import core 

class DjangoAutoUserConfig(AppConfig):
    name = 'dau'
    verbose_name = "Django Auto User"
    def ready(self):
        signals.post_migrate.connect(core.post_migrate_receiver,sender=apps.get_app_config("auth"))
    

