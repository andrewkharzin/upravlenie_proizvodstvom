from django.apps import AppConfig


class SkladConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sklad'

    class Meta:
        verbose_name = "УС Склад"
