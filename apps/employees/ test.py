from django.db import models
from django.db.models import F, Sum
from apps.sklad.order.models.service_class import Service
from django.db.models.signals import post_save
from django.dispatch import receiver

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
    icon  = models.ImageField(upload_to="services/icons", null=True, blank=True)
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    initial_cost = models.DecimalField(_("Базовая цена"), max_digits=10, decimal_places=2, default="10.0")
    price_for_work = models.DecimalField(_("Учетная цена"), max_digits=10, decimal_places=2, default="0.0")
    

    class MPTTMeta:
        order_insertion_by = ['name']

    def get_total_cost(self):
        # Calculate the total cost based on OrderService instances
        return sum(order_service.quantity * order_service.price for order_service in self.orderservice_set.all())

    def __str__(self):
        total_cost = self.get_total_cost()
        return f"{self.name} - { self.initial_cost}"
    


class Employee(models.Model):

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    hired_date = models.DateField()


    def __str__(self):
        return self.name

class WorkShift(models.Model):
    class Meta:
        verbose_name = "Рабочий график"
        verbose_name_plural = "Рабочие графики"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

class Salary(models.Model):

    class Meta:
        verbose_name = "Зарплата"
        verbose_name_plural = "Зарплаты"

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField()

    def get_total_salary(self):
        total_salary = 0
        work_orders = WorkOrder.objects.filter(employee=self.employee, date__month=self.date.month, date__year=self.date.year)
        for work_order in work_orders:
            total_salary += work_order.get_total_cost()
        return total_salary

    def save(self, *args, **kwargs):
        self.amount = self.get_total_salary()
        super().save(*args, **kwargs)

class WorkOrder(models.Model):

    class Meta:
        verbose_name = "Наряд"
        verbose_name_plural = "Наряды"


    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    order_number = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    services = models.ManyToManyField(Service, through='WorkOrderService')
    total_amount = models.DecimalField(
        verbose_name="К выплате:",
        max_digits=10,
        decimal_places=2,
        default=0.0
    )


    def calculate_total_amount(self):
        total_amount = 0
        work_order_services = self.workorderservice_set.all()
        for work_order_service in work_order_services:
            total_amount += work_order_service.service.price_for_work * work_order_service.quantity
        return total_amount
    
    def save(self, *args, **kwargs):
        if self.total_amount is None:
            self.total_amount = self.calculate_total_amount()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee.name}-{self.order_number}-{self.date}|{self.total_amount}"
    
@receiver(post_save, sender='WorkOrderService')
def update_work_order_total_amount(sender, instance, **kwargs):
    instance.work_order.total_amount = instance.work_order.calculate_total_amount()
    instance.work_order.save()

class WorkOrderService(models.Model):
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.service.name} - {self.get_total_price()}"
    
@receiver(post_save, sender=WorkOrderService)
def update_work_order_service_price(sender, instance, **kwargs):
    total_price = instance.service.price_for_work * instance.quantity
    WorkOrderService.objects.filter(pk=instance.pk).update(price=total_price)
