from django.apps import AppConfig


class  MaterialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sklad.materials'
    verbose_name = 'Управление материалами'

    class Meta:
        verbose_name = "Материалы"
