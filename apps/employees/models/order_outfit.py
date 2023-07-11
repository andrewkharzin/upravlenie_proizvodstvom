from django.db import models
from django.db.models import F, Sum
from .employee import EmplEvent, Employee
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from apps.sklad.order.models.service_class import Service
from django.utils.translation import gettext_lazy as _


class WorkOrder(models.Model):

    class Meta:
        verbose_name = "Заказ наряд"
        verbose_name_plural = "Заказ наряды"

    STATUS_CHOICES = [
        ('UNAPPROVED', 'Неутвержден'),
        ('APPROVED', 'Утвержден'),
        ('черновик', 'Черновик'),
    ]

    code = models.CharField(
        max_length=10, unique=True, editable=False, null=True, blank=True)
    employee = models.ForeignKey(
        Employee,  on_delete=models.CASCADE, verbose_name="Ответственный исполнитель")
    services = models.ManyToManyField(Service, through='WorkOrderService')
    date = models.DateField(verbose_name="Дата")
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='Черновик', verbose_name="Статус")

    def create_calendar_event(self):
        services_list = ", ".join(str(service)
                                  for service in self.services.all())
        description = f"Наряд на выполнение следующих работ: {services_list}"
        event = EmplEvent(
            event_type='work_order',
            event_title=f"Заказ наряд для: {self.employee.name}",
            start=self.date,
            end=self.date,
            event_description=description,
        )
        event.save()

    def save(self, *args, **kwargs):
        if not self.pk:  # Generate code only for new instances
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)
        self.create_calendar_event()

    def generate_unique_code(self):
        employee_initials = "".join(word[0]
                                    for word in self.employee.name.split())
        sequential_number = WorkOrder.objects.count() + 1
        sequential_number_str = str(sequential_number).zfill(6)
        return f"{self.date.strftime('%Y%m%d')}-{employee_initials}-{sequential_number_str}"

    def calculate_total_amount(self):
        total_amount = self.services.aggregate(total=Sum('cost'))['total'] or 0
        return total_amount


class WorkOrderService(models.Model):

    class Meta:
        verbose_name = "Задание"
        verbose_name_plural = "Задания"

    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    service = models.ForeignKey(
        Service, on_delete=models.CASCADE, verbose_name="Задача", null=True, blank=True)
    quantity = models.PositiveIntegerField(
        default=1, verbose_name="Количество")
    price = models.DecimalField(
        max_digits=10, decimal_places=2, default=0.0, verbose_name="Цена:")
    percentage_value_add_to_price = models.IntegerField(
        verbose_name="Процент от суммы")

    def get_total_price(self):
        return self.quantity * self.price

    def __str__(self):
        return f"{self.service.name} - {self.get_total_price()}"


class WorkOrderStuffIssued(models.Model):

    class Meta:
        verbose_name_plural = "Исполнители"

    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE)
    order_of_master_person_name = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="order_master", null=True, blank=True, verbose_name="Бригадир:")
    order_of_issued_person_name = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="order_issued_person", null=True, blank=True, verbose_name="Наряд выдан:")
    order_accept_person_name = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="order_accept_person", null=True, blank=True, verbose_name="Наряд принял:")
    order_confirmed_preson_name = models.ForeignKey(
        Employee, on_delete=models.CASCADE, related_name="order_confirmed_person", null=True, blank=True, verbose_name="Наряд утвержден")
    rate_completed_task = models.DecimalField(max_digits=3, decimal_places=1, validators=[
                                              MinValueValidator(Decimal('0.1')), MaxValueValidator(Decimal('5'))], default=0.1)
