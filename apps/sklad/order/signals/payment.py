from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.db import models
from ..models.order_class import Payment


@receiver(pre_save, sender=Payment)
def update_payment_amount(sender, instance, **kwargs):
    if not instance.amount and instance.order:
        # Retrieve the related Order instance
        order = instance.order

        # Calculate the services_total from the associated Order
        services_total = order.order_services.aggregate(
            total=models.Sum(models.F('price') * models.F('quantity'))
        )['total']
        instance.amount = services_total or 0
