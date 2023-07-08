from django.db import models
from django.contrib.auth.models import Group
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
from django.db.models.signals import post_save
from django.utils import timezone
from django.utils.text import slugify
from django.dispatch import receiver
from django.db.models.signals import pre_save
from django.urls import reverse
from django.db.models.signals import pre_delete
from decimal import Decimal
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _

def upload_empl_pic_to(instance, filename):
    # Генерация уникального имени файла
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    
    # Формирование пути сохранения файла
    today = datetime.date.today()
    year = today.year
    month = today.month
    day = today.day
    return f"photos/{year}/{month}/{day}/{filename}"

def create_thumbnail(image):
    # Открываем изображение
    img = Image.open(image.path)

    # Создаем превью с размером 100x100 пикселей
    thumb_size = (100, 100)
    img.thumbnail(thumb_size)

    # Определяем путь для сохранения превью
    thumb_path = f"{os.path.splitext(image.path)[0]}_thumb.jpg"

    # Сохраняем превью
    img.save(thumb_path)

    # Возвращаем путь к превью
    return thumb_path

class Employee(models.Model):

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    name = models.CharField(_("ФИО сотрудника"), max_length=100)
    position = models.CharField(_("Должность"), max_length=100)
    hired_date = models.DateField(_("Дата найма"))
    birthday = models.DateField(_("День рождения"))
    photo = models.ImageField(upload_to=upload_empl_pic_to, default="users/default.jpeg")
    photo_thumb = models.ImageField(upload_to=upload_empl_pic_to, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_staff = models.BooleanField(_("Добавить аккаунт?"), default=False)
    rating = models.FloatField(default=0.0) 

    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        
        if self.photo and not self.photo_thumb:
            # Создаем превью фотографии
            thumb_path = create_thumbnail(self.photo)
            
            # Сохраняем путь к превью
            self.photo_thumb = thumb_path
            super().save(*args, **kwargs)
    
    def image_tag(self):
        return format_html('<img src="{}" width="50" height="50" />', self.photo.url)
    image_tag.short_description = 'Фото'

    def thumb_image_tag(self):
        if self.photo_thumb:
            return format_html('<img src="{}" width="50" height="50" />', self.photo_thumb.url)
        else:
            return mark_safe('<span>Нет превью</span>')
    thumb_image_tag.short_description = 'Превью'

    def __str__(self):
        return self.name

# # @receiver(pre_save, sender=Employee)
# def create_birthday_event(sender, instance, created, **kwargs):
#     if created and instance.birthday:
#         calendar_id = 1  # ID календаря "Дни рождения"
#         try:
#             calendar = Calendar.objects.get(id=calendar_id)
#             event = Event.objects.create(
#                 title=f"День рождения {instance.name}",
#                 start=instance.birthday,
#                 end=instance.birthday,
#                 calendar=calendar
#             )
#             event.save()
#         except Calendar.DoesNotExist:
#             pass


# @receiver(pre_save, sender=Employee)
# def create_user(sender, instance, **kwargs):
#     if instance.pk is None and instance.is_staff and not instance.user:
#         username = translit(instance.name.split()[0], 'ru', reversed=True)  # Transliterate the first word of the name
#         email = f"{username}@mycompany.com"  # Generate the email address
#         password = User.objects.make_random_password()
#         user = User.objects.create_user(email=email, password=password)
#         instance.user = user

# @receiver(post_save, sender=Employee)
# def add_employee_to_registered_group(sender, instance, created, **kwargs):
#     if created and instance.is_staff:
#         registered_group, _ = Group.objects.get_or_create(name='Зарегистрированные')
#         instance.user.groups.add(registered_group)

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

    def create_calendar_event(self):
        services_list = ", ".join(str(service) for service in self.services.all())
        description = f"Наряд на выполнение следующих работ: {services_list}"
        event = EmplEvent(
            event_type='work_order',
            event_title=f"Заказ наряд для: {self.employee.name}",
            start=self.date,
            end=self.date,
            event_description=description,
        )
        event.save()

    # def delete(self, *args, **kwargs):
    #     if self.status == 'APPROVED':
    #         raise models.ProtectedError("Approved work orders cannot be deleted.", self)
    #     super().delete(*args, **kwargs)

    def save(self, *args, **kwargs):
        if not self.pk:  # Generate code only for new instances
            self.code = self.generate_unique_code()
        super().save(*args, **kwargs)
        self.create_calendar_event()

    def generate_unique_code(self):
        employee_initials = "".join(word[0] for word in self.employee.name.split())
        sequential_number = WorkOrder.objects.count() + 1
        sequential_number_str = str(sequential_number).zfill(6)
        return f"{self.date.strftime('%Y%m%d')}-{employee_initials}-{sequential_number_str}"

    def calculate_total_amount(self):
        total_amount = self.services.aggregate(total=Sum('cost'))['total'] or 0
        return total_amount
    
@receiver(post_save, sender=WorkOrder)
def create_work_order_calendar_event(sender, instance, created, **kwargs):
    if created:
        instance.create_calendar_event()
    
    
# @receiver(pre_delete, sender=WorkOrder)
# def protect_approved_work_order(sender, instance, **kwargs):
#     if instance.status == 'APPROVED':
#         raise models.ProtectedError("Approved work orders cannot be deleted.", instance)

class WorkOrderService(models.Model):

    class Meta:
        verbose_name = "Работа"
        verbose_name_plural = "Работы"

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
    


class EmplEvent(Event):

    class Meta:
        verbose_name_plural = "Cобытия"
        

    event_type_choices = [
        ('наряд', 'Наряд'),
        ('встреча', 'Встреча'),
        ('заказ', 'Заказ'),
        ('день рождения', 'День рождения'),
        ('учет', 'Учет'),
        ('прочее', 'Прочее'),
    ]
    
    title = None
    description = None
    
    event_type = models.CharField(_("Тип события"), max_length=30, choices=event_type_choices, default="прочее")
    event_title = models.CharField(_("Название"),  max_length=100)
    event_description = models.TextField(_("Описание"), blank=True)
   
    def save(self, *args, **kwargs):
        # Получите объект календаря с id=1
        calendar = Calendar.objects.get(id=2)
        
        # Присвойте полю calendar значение календаря
        self.calendar = calendar
        
        # Сохраните событие
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('employees:calendar_event_detail', args=[str(self.id)])

    def __str__(self):
        return self.title
