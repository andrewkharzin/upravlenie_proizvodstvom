import os
from datetime import datetime
import qrcode
from django.db.models import F, Sum
from django.db.models.signals import pre_save
from django.dispatch import receiver
from decimal import Decimal
from django.db.models import DecimalField
import json
from django.db.models.signals import post_save
from django.dispatch import receiver
from .invoice_class import Invoice
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.db import models
from apps.accounts.models import User
# from apps.sklad.materials.models.material_class import Material
from apps.sklad.inventory.models.inventory import InventoryItem
from django.utils.translation import gettext_lazy as _
from django import forms
from django.utils import timezone
import qrcode
from django.core.files import File
from django.urls import reverse
from io import BytesIO
from .service_class import Service
from ..utility.generate_order_qr import generate_qr_code

Material = "materials.Material"

class OrderService(models.Model):

    class Meta:
        verbose_name_plural = "Заказанные услуги"
        
    order = models.ForeignKey('Order', on_delete=models.CASCADE, related_name='order_services')
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    price = models.DecimalField(_("Стоимость"), max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(_("Количество"))

    def __str__(self):
        return f"{self.service.name}"
    
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Calculate the total amount for the associated order
        order = self.order
        services_total = order.order_services.aggregate(
                total=models.Sum(F('price') * F('quantity'))
            )['total']

        # Update the amount in the associated payment
        payment = order.payment
        if payment:
                payment.amount = services_total
                payment.save()

@receiver(post_save, sender=OrderService)
def update_payment_total(sender, instance, created, **kwargs):
    # Trigger the update of payment total when an OrderService is saved
    if not created:
        instance.order.save()
    
def customer_function():
    from apps.sklad.order.models.customer_class import Customer

    # Use MyClass here within the function
    obj = Customer()
    Customer = obj
    # obj.some_method()



class Order(models.Model):

    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    ORDER_TYPE = (
        ("изготовление памятника",  "Изготовление памятника"),
        ("комплекс",  "Комплекс"),
    )
    ORDER_STATUS = (
        ("заказ принят", "Заказ принят"),
        ("передан в работу", "Передан в работу"),
        ("изготовление", "Изготовление"),
        ("изготовлено", "Изготовлено"),
        ("работы выполнены", "Работы выполнены")
    )
    order_type = models.CharField(_("Тип заказа"), max_length=30, choices=ORDER_TYPE)
    materials = models.ManyToManyField('materials.Material', through='OrderMaterial', related_name="order_materials")
    services = models.ManyToManyField(Service, through=OrderService)
    customer = models.ForeignKey('Customer', on_delete=models.PROTECT, related_name="customer_order", blank=True, null=True)
    deadline = models.DateField(_("Срок услуги"), null=True, blank=True)
    epitaph = models.TextField(_("Эпитафия"), blank=True, null=True)
    description = models.TextField(_("Детали заказа"), blank=True, null=True)
    order_stuff = models.ManyToManyField('OrderStuff', through='OrderStuffFile', related_name='order_stuff_set')
    order_date = models.DateField(default=timezone.now)
    order_number = models.CharField(max_length=6, unique=True, editable=False)
    order_status = models.CharField(max_length=80, choices=ORDER_STATUS, default="новый заказ")
    qr_code_image = models.ImageField(upload_to='orders/qr_codes/', blank=True, null=True, editable=False)
    

    create_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    update_at = models.DateTimeField(auto_now_add=True)
    # Другие поля заказа


    def update_invoice_data(self):
        invoice = self.invoice
        order_services = self.order_services.all()
        services_total = order_services.aggregate(
            total=models.Sum(F('price') * F('quantity'))
        )['total']
        invoice.amount = services_total

         # Добавление Service_total в контекст
        context = {
            'invoice': invoice,
            'Service_total': services_total,
        }
        invoice.save()
        return context

    def update_inventory(self):
        order_materials = self.order_materials.select_related('material')
        for order_material in order_materials:
            material = order_material.material
            quantity = order_material.quantity
            material.inventory.quantity = F('quantity') - quantity
            material.inventory.save()

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.annotate(
            inventory_quantity=models.Sum('material__inventory__items__received_quantity')
        ).filter(inventory_quantity__gt=0)
    
    def formfield(self, **kwargs):
     defaults = {
        'form_class': forms.ModelChoiceField,
        'queryset': Material.objects.filter(inventory__quantity__gt=0),
        'limit_choices_to': {'inventory__quantity__gt': 0},
    }
     defaults.update(kwargs)
     return super().formfield(**defaults)



    def save(self, *args, **kwargs):
        if not self.order_number:
            last_order = Order.objects.order_by('-id').first()
            last_number = int(last_order.order_number) if last_order else 0
            self.order_number = str(last_number + 1).zfill(5)
            generate_qr_code(self)

        # Validate the model and save the 'Order' instance
        self.full_clean()
        super().save(*args, **kwargs)

        # Access the related services after saving the order
        services_total = self.order_services.aggregate(
            total=Sum(F("quantity") * F("price"), output_field=DecimalField())
        )["total"]

        if services_total:
            self.services_total = services_total
        else:
            self.services_total = Decimal(0)

        # Update the amount in the associated invoice
        if self.invoice:
            self.invoice.amount = services_total or 0
            self.invoice.save()

        self.total = self.services_total

        # Save the 'Order' instance again with updated values
        super().save(*args, **kwargs)

        # Update the inventory after saving the order
        self.update_inventory()





    @receiver(post_save, sender='order.Order')
    def create_or_update_invoice(sender, instance, created, **kwargs):
        if created:
            # Create a new invoice
            Invoice.objects.create(order=instance)
        else:
            # Update the existing invoice
            instance.invoice.update_invoice_data()

    

    def __str__(self):
        return f"Заказ #{self.order_number} для {self.customer}"
    
def order_file_path(instance, filename):
    today = datetime.today()
    year = str(today.year)
    month = today.strftime('%m')
    order_number = str(instance.order.order_number).zfill(6)
    return os.path.join('order_files', year, month, order_number, filename)

class OrderMaterial(models.Model):


    class Meta:
        verbose_name = "Материал"
        verbose_name_plural = "Материалы"

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_materials')
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.material} - {self.quantity}"

class OrderFile(models.Model):
    # Your file fields here
    order_file = models.FileField(upload_to=order_file_path)
    file_description = models.CharField(max_length=255, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='files')

    def __str__(self):
        return f'Order File {self.id}'
    
class OrderStuff(models.Model):
    class Meta:
        verbose_name = "Файл картинки"
        verbose_name_plural = "Файлы картинок"
        
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='stuff')
    stuff_files = models.ManyToManyField(OrderFile, through='OrderStuffFile')
    stuff_image = models.ImageField(upload_to=order_file_path, null=True, blank=True)
    image_description = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return f'Order Stuff {self.id}'


class OrderStuffFile(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    order_stuff = models.ForeignKey(OrderStuff, on_delete=models.CASCADE)
    order_file = models.ForeignKey(OrderFile, on_delete=models.CASCADE)
    file_description = models.CharField(max_length=255)

    class Meta:
        verbose_name = "Order Stuff File"
        verbose_name_plural = "Order Stuff Files"




class Shipping(models.Model):
    class Meta:
        verbose_name = "Доставка"

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='shipping')
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=20)

    def __str__(self):
        return f'Shipping for {self.order}'

class Payment(models.Model):
    class Meta:
        verbose_name_plural = "Способ оплаты"

    PAY_METHOD = (
        ('наличные', 'Наличные'),
        ('банковской картой', 'Банковской картой'),
        ('банковский перевод', 'Банковский перевод'),
    )

    order = models.OneToOneField(Order, on_delete=models.CASCADE, related_name='payment')
    method = models.CharField(max_length=50, choices=PAY_METHOD,default="Наличные")
    amount = models.DecimalField(max_digits=10, decimal_places=2, )
    transaction_id = models.CharField(max_length=100, null=True, blank=True)
        

    def __str__(self):
        return f'Payment for {self.order}'


