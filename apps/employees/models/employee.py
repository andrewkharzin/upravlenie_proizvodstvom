from django.db import models
from schedule.models import Event, Calendar
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from apps.accounts.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext_lazy as _
from ..utils.helper_funcs import create_thumbnail, upload_empl_pic_to

class Employee(models.Model):

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"

    ROLE = (
        ('рабочий', 'Рабочий'),
        ('бригадир', 'Бригадир'),
        ('руководитель', 'Руководитель'),
        ('специалист', 'Специалист'),
        ('уборщик', 'Уборщик'),
        ('продавец', 'Продавец'),
        ('охранник', 'Охранник'),
    )


    role = models.CharField(verbose_name="роль", max_length=50, choices=ROLE, default="Рабочий")
    name = models.CharField(_("ФИО сотрудника"), max_length=100)
    position = models.CharField(_("Должность"), max_length=100)
    hired_date = models.DateField(_("Дата найма"))
    birthday = models.DateField(_("День рождения"))
    photo = models.ImageField(
        upload_to=upload_empl_pic_to, default="users/default.jpeg")
    photo_thumb = models.ImageField(upload_to=upload_empl_pic_to, blank=True)
    phone = PhoneNumberField(null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    is_staff = models.BooleanField(_("Добавить аккаунт?"), default=False)
    rating = models.FloatField(default=0.0)

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)

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

    event_type = models.CharField(
        _("Тип события"), max_length=30, choices=event_type_choices, default="прочее")
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