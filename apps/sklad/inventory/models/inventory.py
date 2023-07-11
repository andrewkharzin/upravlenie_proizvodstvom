from django.db import models
from apps.accounts.models import User
from django.utils import timezone
from django.template.defaultfilters import slugify
# from apps.sklad.materials.models.material_class import Material 
from openpyxl import Workbook
from apps.accounts.models import User
from django.utils.translation import gettext_lazy as _


class Inventory(models.Model):

    class Meta:
        verbose_name_plural = "Инвентаризация"

    REASON_CHOICES = (
        ('первичная', 'Первиная'),
        ('повторная', 'Повторная'),
        ('Списание', 'Списание'),
    )

    material = models.ForeignKey(
        'materials.Material',
        on_delete=models.CASCADE,
        related_name='inventories'
    )
    # materials = models.ManyToManyField('materials.Material', related_name='inventories')
    inv_number = models.CharField(max_length=50, unique=True, editable=False)
    description = models.TextField(blank=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_modified = models.DateTimeField(auto_now=True)
    reason = models.CharField(max_length=20, choices=REASON_CHOICES)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def material_info(self):
        property_values = ', '.join(str(property) for property in self.material.properties.all())
        return f"{self.material.name} - {self.material.material_type} - {property_values}"

    def generate_inv_number(self):
        inv_type = ""
        if self.reason == "первичная":
            inv_type = "ИНВ"
        elif self.reason == "повторная":
            inv_type = "ИНП"
        elif self.reason == "Списание":
            inv_type = "ИНС"
        date = self.date_created.strftime("%d%m%Y")
        unique_id = str(self.id).zfill(6)
        return f"{inv_type}-{date}-{unique_id}"

    def __str__(self):

        return f"Инвентаризация ({self.date_created} - {self.user.username})"

    def save(self, *args, **kwargs):
        if not self.inv_number:
            super().save(*args, **kwargs)  # Сохраняем модель для генерации уникального id
            self.inv_number = self.generate_inv_number()
            self.save()  # Сохраняем с присвоенным inv_number
        else:
            super().save(*args, **kwargs)
        InventoryHistory.objects.create(inventory=self, reason='Modified')

    def delete(self, *args, **kwargs):
        InventoryHistory.objects.create(inventory=self, reason='Deleted')
        super().delete(*args, **kwargs)
    

class InventoryItem(models.Model):

    class Meta:
        verbose_name_plural = "Позиции"

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='items')
    received_quantity = models.IntegerField(default=0)
    responsible_person = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='responsible_items')
    received_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='received_items')
    received_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.inventory.material} - {self.received_quantity}"
    
    def get_stock_quantity(self):
        return self.received_quantity - self.reduced_quantity

    def get_quantity_after_inventory(self):
        # Calculate the quantity after inventory processing
        quantity_after_inventory = self.received_quantity - self.inventory.reduced_quantity

        return quantity_after_inventory


class InventoryHistory(models.Model):

    class Meta:
        verbose_name_plural = "Трэкинг" 

    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='history_entries')
    date_modified = models.DateTimeField(auto_now=True)
    reason = models.CharField(max_length=20, choices=Inventory.REASON_CHOICES)

    def __str__(self):
        return f"Inventory History - {self.inventory} - {self.date_modified}"