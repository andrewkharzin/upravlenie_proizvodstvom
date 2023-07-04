from django.apps import AppConfig


class  MaterialConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.sklad.order'
    verbose_name = 'Управление заказами и клиентами'

    def ready(self):
        # import apps.sklad.order.signals.invoice_sgnl
        import apps.sklad.order.signals.payment

    
