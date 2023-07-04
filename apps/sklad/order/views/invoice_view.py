from django.shortcuts import render
from ..models.invoice_class import Invoice
from ..models.order_class import Order

def invoice_list(request):
    order = Order.objects.all()
    invoices = Invoice.objects.all()
    page_title = 'Счета клиентов'

    context = {
        'order': order,
        'invoices': invoices,
        'page_title': page_title
    }
    return render(request, 'invoices/invoice_list.html', context)