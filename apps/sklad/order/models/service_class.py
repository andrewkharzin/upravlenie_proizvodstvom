import os
from datetime import datetime
from django.db import models
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.translation import gettext_lazy as _


class Service(MPTTModel):
    class Meta:
        verbose_name = "Наминклатура услуг"
        verbose_name_plural = "Наминклатура услуг"

    name = models.CharField(_("Название услуги"), max_length=255)
    icon = models.ImageField(upload_to="services/icons", null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE,
                            null=True, blank=True, related_name='children')
    initial_cost = models.DecimalField(
        _("Базовая цена"), max_digits=10, decimal_places=2, default="10.0")
    price_for_work = models.DecimalField(
        _("Учетная цена"), max_digits=10, decimal_places=2, default="0.0")
    percentage_from_base = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
        verbose_name='Percentage'
    )

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_total_cost(self):
        # Calculate the total cost based on OrderService instances
        return sum(order_service.quantity * order_service.price for order_service in self.orderservice_set.all())

    def __str__(self):
        total_cost = self.get_total_cost()
        return f"{self.name} - { self.initial_cost}"
