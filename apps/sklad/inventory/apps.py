from django.apps import AppConfig


class  MaterialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sklad.inventory'
    verbose_name = 'Инвентаризация и учет'

