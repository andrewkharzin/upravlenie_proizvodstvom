from django.db import models
from django.contrib.auth.models import Group
from datetime import date, timedelta
from django.core.exceptions import ValidationError
import os
import uuid
import datetime
from PIL import Image
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from transliterate import translit
from apps.accounts.models import User
from schedule.models import Event, Calendar
from django.db.models import F, Sum
from apps.sklad.order.models.service_class import Service
from django.utils import timezone
from django.utils.text import slugify
from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from .employee import EmplEvent, Employee


class WorkShift(models.Model):
    class Meta:
        verbose_name_plural = "Рабочие графики"

    SHIFT_TYPES = (
        ('day', 'Day Shift'),
        ('night', 'Night Shift'),
    )

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    shift_type = models.CharField(
        _("Режим"), max_length=10, choices=SHIFT_TYPES, default="day")
    vacation = models.BooleanField(_("Отпуск"), default=False)
    start_date = models.DateField(_("Начало"), blank=True, null=True)
    end_date = models.DateField(_("Окончание"), blank=True, null=True)
    work_days = models.PositiveIntegerField(
        _("Рабочие дни"), blank=True, null=True)

    def save(self, *args, **kwargs):
        if self.start_date and self.end_date:
            total_days = (self.end_date - self.start_date).days + 1
            weekends = 0
            current_date = self.start_date
            while current_date <= self.end_date:
                # Исключаем субботу (5) и воскресенье (6)
                if current_date.weekday() not in [5, 6]:
                    weekends += 1
                current_date += timedelta(days=1)

            self.work_days = weekends

            super().save(*args, **kwargs)

    def __str__(self):
        return f"Shift for {self.employee.name}"


class Salary(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date_from = models.DateField(_("От"))
    date_to = models.DateField(_("До"))
    bonus = models.DecimalField(
        _("Премия"), max_digits=10, decimal_places=2, default=Decimal('0.00'))
    advance = models.DecimalField(
        _("Аванс"), max_digits=10, decimal_places=2, default=Decimal('0.00'))
    total_salary = models.DecimalField(
        _("Итого к выплате:"), max_digits=10, decimal_places=2)
    issued = models.BooleanField(_("Выдано"), default=False)
    code = models.CharField(max_length=20, unique=True,
                            editable=False, null=True, blank=True)

    def __str__(self):
        return f"Зарплата для сотрудника {self.employee.name} на период с {self.date_from} по {self.date_to} - К выплате {self.total_salary} - за вычетом аванса {self.advance}"

    def calculate_total_salary(self):
        approved_work_orders = self.employee.workorder_set.filter(
            status='APPROVED')
        total_amount = Decimal(0)
        for work_order in approved_work_orders:
            services = work_order.services.all()
            for service in services:
                total_amount += service.price_for_work * \
                    service.workorderservice_set.get(
                        work_order=work_order).quantity
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
            max_code = Salary.objects.aggregate(
                models.Max("code"))["code__max"]
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
