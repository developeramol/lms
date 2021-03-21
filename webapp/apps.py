from django.apps import AppConfig
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from .signals import create_user_profile, save_user_profile, create_client_profile, save_client_profile


class WebappConfig(AppConfig):
    name = 'webapp'

    def ready(self):
        post_save.connect(create_user_profile, sender=User)
        post_save.connect(save_user_profile, sender=User)
        post_save.connect(create_client_profile, sender=User)
        post_save.connect(save_client_profile, sender=User)
