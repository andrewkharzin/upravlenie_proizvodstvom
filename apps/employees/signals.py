from django.db.models.signals import pre_save
from django.db.models.signals import post_save
from django.contrib.auth.models import Group
from django.urls import reverse
from django.dispatch import receiver
from transliterate import translit
from apps.employees.models import Employee
from schedule.models import Calendar, Event
from apps.accounts.models import User

@receiver(pre_save, sender=Employee)
def create_birthday_event(sender, instance, **kwargs):
    if instance.pk is None and instance.birthday:
        calendar_id = 1  # ID календаря "Дни рождения"
        try:
            calendar = Calendar.objects.get(id=calendar_id)
            event = Event.objects.create(
                title=f"День рождения {instance.name}",
                start=instance.birthday,
                end=instance.birthday,
                calendar=calendar
            )
            event.save()
        except Calendar.DoesNotExist:
            pass


@receiver(pre_save, sender=Employee)
def create_user(sender, instance, **kwargs):
    if instance.pk is None and instance.is_staff and not instance.user:
        username = translit(instance.name.split()[0], 'ru', reversed=True)  # Transliterate the first word of the name
        email = f"{username}@mycompany.com"  # Generate the email address
        password = User.objects.make_random_password()
        user = User.objects.create_user(email=email, password=password)
        instance.user = user


@receiver(post_save, sender=Employee)
def add_employee_to_registered_group(sender, instance, created, **kwargs):
    if created and instance.is_staff:
        registered_group, _ = Group.objects.get_or_create(name='Зарегистрированные')
        instance.user.groups.add(registered_group)