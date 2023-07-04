from django.db.models.signals import post_save
from django.dispatch import receiver
from ..models.invoice_class import Invoice
from ..models.customer_class import Customer

@receiver(post_save, sender=Customer)
def create_invoice(sender, instance, created, **kwargs):
    if created:
        # Create a new invoice for the customer
        invoice = Invoice.objects.create(customer=instance)

        # Generate the Excel file for the invoice using the template

        # Save the Excel file to a desired location

        # You can also perform any additional actions here, such as sending the invoice via email, etc.
