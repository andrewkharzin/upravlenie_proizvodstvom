from django.core.exceptions import ValidationError
import uuid
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .customer_class import Customer
from .service_class import Service



class Invoice(models.Model):
    class Meta:
        verbose_name = "Счет"
        verbose_name_plural = "Счета"

    order = models.OneToOneField('order.Order', on_delete=models.PROTECT)
    customer = models.ForeignKey(Customer, on_delete=models.PROTECT, null=True)
    date = models.DateField(_("Дата"), default=timezone.now)
    amount = models.DecimalField(_("Итого к оплате"), max_digits=10, decimal_places=2, null=True)
    advance_payment = models.DecimalField(_("Авансовый платеж"), max_digits=10, decimal_places=2, default=0)
    balance_due = models.DecimalField(_("Остаток к оплате"), max_digits=10, decimal_places=2, default=0, editable=False)
    bill_closed = models.BooleanField(default=False)
    invoice_number = models.CharField(max_length=20, unique=True, editable=False, default="")


# ...

    def generate_invoice_number(self):
        today = timezone.now().date()
        invoices_today = Invoice.objects.filter(date=today)
        count = invoices_today.count() + 1
        invoice_number = f"№{today}-{str(count).zfill(5)}"
        
        # Check if the generated invoice number already exists
        if Invoice.objects.filter(invoice_number=invoice_number).exists():
            raise ValidationError("Duplicate invoice number generated. Please try again.")

        return invoice_number

    
    def update_invoice_data(self):
        self.order.update_invoice_data()

    def update_balance_due(self):
        self.balance_due = (self.amount or 0) - self.advance_payment
        

    def save(self, *args, **kwargs):
        if not self.pk:
            # New instance, calculate the balance due
            self.update_balance_due()
        if not self.invoice_number:
            self.invoice_number = self.generate_invoice_number()
        super().save(*args, **kwargs)

        # Update balance due after saving the instance
        self.update_balance_due()
        super().save(update_fields=['balance_due'])


    

    def __str__(self):
        return f"Счет для {self.customer}"