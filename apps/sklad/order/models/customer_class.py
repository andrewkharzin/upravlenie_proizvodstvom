import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
# from apps.sklad.order.models.order_class import Order

def customer_image_directory_path(instance, filename):
    # Upload the customer's image to a specific directory
    return f'customer_images/{instance.pk}/{filename}'


class Customer(models.Model):

    class Meta:
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

    CLIENT_TYPES = (
        ('Ч', 'Частный клиент'),
        ('К', 'Контрагент'),
    )
    client_type = models.CharField(max_length=1, choices=CLIENT_TYPES, default="")
    registered_year = models.IntegerField(default=timezone.now().year)
    counter = models.IntegerField(default=0, editable=False)
    image = models.ImageField(upload_to=customer_image_directory_path, default='customers/images/default_image.png')
    
    # Other fields in your Customer model
    name = models.CharField(_("ФИО Клиента"), max_length=120)
    # order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="customer_order")
    city = models.CharField(_("Город"), max_length=20, null=True, blank=True)
    street = models.CharField(_("Улица"), max_length=50, null=True, blank=True)
    phone  = models.CharField(_("Телефон контактный"), max_length=15, null=True, blank=True)
   
    # Другие поля заказчика

    def save(self, *args, **kwargs):
        if not self.id:
            # Increment the counter
            last_customer = Customer.objects.filter(client_type=self.client_type, registered_year=self.registered_year).order_by('-counter').first()
            if last_customer:
                self.counter = last_customer.counter + 1

        super().save(*args, **kwargs)

    @property
    def customer_id(self):
        return f"{self.client_type}{self.registered_year}-{str(self.counter).zfill(6)}"

    def __str__(self):
        return f"{self.customer_id}/{self.name}"




class Passport(models.Model):
    class Meta:
        verbose_name = "Паспорт"
        verbose_name_plural = "Паспорта клиентов"

    customer = models.OneToOneField(Customer, on_delete=models.CASCADE)
    passport_number_series = models.CharField(_("Серия паспорта"), max_length=4)
    passport_number = models.CharField(_("Номер паспорта"), max_length=6)
    passport_issued_by = models.CharField(_("Кем выдан паспорт"), max_length=100)
    passport_issue_date = models.DateField(_("Дата выдачи паспорта"))
    division_code = models.CharField(_("Код подразделения"), max_length=7)

    def __str__(self):
        return f"Passport for {self.customer.name}"





