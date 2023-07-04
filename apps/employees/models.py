from django.db import models
from django.db.models import F, Sum
from apps.sklad.order.models.service_class import Service
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_delete
from decimal import Decimal
from django.utils.translation import gettext_lazy as _


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
        verbose_name_plural = "Рабочие графики"

    SHIFT_TYPES = (
        ('day', 'Day Shift'),
        ('night', 'Night Shift'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift_type = models.CharField(_("Режим"), max_length=10, choices=SHIFT_TYPES, default="day")
    start_date = models.DateField(_("Начало"), blank=True, null=True)
    end_date = models.DateField(_("Окончание"), blank=True, null=True)
    planned_schedule = models.TextField(_("Планируемый график"), blank=True, null=True)
    vacation = models.BooleanField(_("Отпуск"), default=False)
    calendar_event = models.CharField(_("Событие"), max_length=100, blank=True)

    def __str__(self):
        return f"{self.get_shift_type_display()} Shift for {self.employee.name} - {self.start_date} to {self.end_date}"




class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_from = models.DateField(_("От"))
    date_to = models.DateField(_("До"))
    bonus = models.DecimalField(_("Премия"), max_digits=10, decimal_places=2, default=Decimal('0.00'))
    advance = models.DecimalField(_("Аванс"), max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_salary = models.DecimalField(_("Итого к выплате:"), max_digits=10, decimal_places=2)
    issued = models.BooleanField(_("Выдано"), default=False)
    code = models.CharField(max_length=20, unique=True, editable=False, null=True, blank=True)

    def __str__(self):
     return f"Зарплата для сотрудника {self.employee.name} на период с {self.date_from} по {self.date_to} - К выплате {self.total_salary} - за вычетом аванса {self.advance}"

    def calculate_total_salary(self):
        approved_work_orders = self.employee.workorder_set.filter(status='APPROVED')
        total_amount = Decimal(0)
        for work_order in approved_work_orders:
            services = work_order.services.all()
            for service in services:
                total_amount += service.price_for_work * service.workorderservice_set.get(work_order=work_order).quantity
        total_amount += self.bonus
        total_amount -= self.advance
        return total_amount
    
    @property
    def total_salary_rub(self):
        return f"{self.total_salary} ₽"
    
    def save(self, *args, **kwargs):
        if not self.code:
            # Generate the unique code
            date_part = timezone.now().strftime("%Y%m%d")
            fio_part = slugify(self.employee.name).upper()
            max_code = Salary.objects.aggregate(models.Max("code"))["code__max"]
            if max_code:
                max_code_num = int(max_code[-6:])
                new_code_num = max_code_num + 1
            else:
                new_code_num = 1
            code_part = str(new_code_num).zfill(6)
            self.code = f"{date_part}-ЗП-{fio_part}-{code_part}"

        super().save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Зарплаты"


class WorkOrder(models.Model):

    class Meta:
        verbose_name = "Заказ наряд"
        verbose_name_plural = "Заказ наряды"

    STATUS_CHOICES = [
        ('UNAPPROVED', 'Неутвержден'),
        ('APPROVED', 'Утвержден'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    services = models.ManyToManyField(Service, through='WorkOrderService')
    date = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='UNAPPROVED')
    code = models.CharField(max_length=10, unique=True, editable=False, null=True, blank=True)

    def delete(self, *args, **kwargs):
        if self.status == 'APPROVED':
            raise models.ProtectedError("Approved work orders cannot be deleted.", self)
        super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.pk:  # Generate code only for new instances
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)

    def generate_unique_code(self):
        employee_initials = "".join(word[0] for word in self.employee.name.split())
        sequential_number = WorkOrder.objects.count() + 1
        sequential_number_str = str(sequential_number).zfill(6)
        return f"{self.date.strftime('%Y%m%d')}-{employee_initials}-{sequential_number_str}"

    def calculate_total_amount(self):
        total_amount = self.services.aggregate(total=Sum('cost'))['total'] or 0
        return total_amount
    
@receiver(pre_delete, sender=WorkOrder)
def protect_approved_work_order(sender, instance, **kwargs):
    if instance.status == 'APPROVED':
        raise models.ProtectedError("Approved work orders cannot be deleted.", instance)

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
    


class CalendarEvent(models.Model):
    class Meta:
        verbose_name_plural = "Календарь"

    event_type_choices = [
        ('meeting', 'Meeting'),
        ('holiday', 'Holiday'),
        ('birthday', 'Birthday'),
        ('other', 'Other'),
    ]

    event_type = models.CharField(_("Тип события"), max_length=10, choices=event_type_choices)
    title = models.CharField(_("Название"),  max_length=100)
    start_date = models.DateField(_("Начало"), null=True, blank=True)
    end_date = models.DateField(_("Окончание"), null=True, blank=True)
    description = models.TextField(_("Описание"), blank=True)

    def __str__(self):
        return self.title