import os
import uuid
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from apps.sklad.order.models.order_class import Order
# from apps.sklad.inventory.models.inventory import InventoryItem
class MaterialType(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Тип материала"
        verbose_name_plural = "Типы материалов"


    def __str__(self):
        return self.name
    
def material_image_upload_path(instance, filename):
    # Генерируем уникальное имя файла с помощью модуля uuid
    unique_filename = f"{uuid.uuid4().hex}{os.path.splitext(filename)[1]}"
    # Определяем путь загрузки в зависимости от даты и типа материала
    upload_path = f"materials/{instance.date_created.year}/{instance.material_type}/{unique_filename}"
    return upload_path
    

class Material(models.Model):

    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"
    # inventory = models.OneToOneField(
    #     'inventory.InventoryItem',  # Use string reference instead of direct import
    #     on_delete=models.CASCADE
    # )
    order = models.ForeignKey(Order, on_delete=models.CASCADE, blank=True, null=True, editable=False)
    name = models.CharField(max_length=100)
    material_type = models.ForeignKey(MaterialType, on_delete=models.CASCADE)
    properties = GenericRelation('Property')
    image = models.ImageField(upload_to=material_image_upload_path, blank=True, null=True)
    date_created = models.DateField(auto_now=True)
    purchase_price = models.DecimalField(_("Цена закупки"), max_digits=10, decimal_places=2, default="0.0")
    
   
    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

    def __str__(self):
        properties = ', '.join(str(property) for property in self.properties.all())
        return f"{self.name} - {self.material_type} - {properties}"

class Property(models.Model):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    name = models.CharField(max_length=100)
    value = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Свойство материала"
        verbose_name_plural = "Свойства материалов"

    def __str__(self):
        return f"{self.name}/{self.value}"
