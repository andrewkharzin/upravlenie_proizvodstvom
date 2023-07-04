import qrcode
from django.views import View
from django.shortcuts import render, get_object_or_404, redirect
from ..forms_base import CustomerForm
from django.http import HttpResponse
from io import BytesIO
from ..models.order_class import Order
from django.views.generic.edit import DeleteView
from django.http import JsonResponse
from django.urls import reverse, NoReverseMatch



from django.shortcuts import render
from ..models.customer_class import Customer
from ..models.order_class import Order
from ..models.invoice_class import Invoice

class CustomerOrdersView(View):
    template_name = 'customers/customer_detail.html'

    def get(self, request, customer_id):
        customer = get_object_or_404(Customer, id=customer_id)
        orders = customer.customer_order.all()
        invoices = Invoice.objects.filter(customer=customer)
        page_title = f'Список заказов {customer.name}'
        customer_detail_url = reverse('order:customer_detail', kwargs={'customer_id': customer_id})
        invoice = Invoice.objects.first()  # Здесь получите объект Invoice, связанный с заказом

        context = {
            'customer': customer,
            'orders': orders,
            'page_title': page_title,
            'invoices': invoices,
            'invoice': invoice, 
            'customer_detail_url': customer_detail_url,
            
        }

        return render(request, self.template_name, context)
# class CustomerOrdersView(View):
#     model = Customer
#     template_name = 'customers/customer_detail.html'
#     context_object_name = 'orders'

#     def get(self, request, customer_id):
#         try:
#             customer = Customer.objects.get(id=customer_id)
#             invoices = Invoice.objects.filter(customer=customer)
#             orders = Order.objects.filter(customer=customer)

#             for order in orders:
#                 print("Order ID:", order.order_number)
#                 print("Customer:", order.customer)
#                 print("Order Date:", order.order_date)

#             for inv in invoices:
#                 print("Сумма счета:", inv.amount)

#             context = {
#                 'customer': customer,
#                 'invoices': invoices,
#                 'orders': orders,
#                 'page_title': f'Список заказов {customer.name}',  # Update the page_title with customer's name
#             }

#             try:
#                 customer_detail_url = reverse('order:customer_detail', kwargs={'customer_id': customer_id})
#                 print("Customer Detail URL:", customer_detail_url)
#             except NoReverseMatch as e:
#                 print("Error in reverse:", str(e))
#                 customer_detail_url = ''

#             context['customer_detail_url'] = customer_detail_url

#             return render(request, self.template_name, context)

#         except Customer.DoesNotExist:
#             return HttpResponse("Customer not found", status=404)

    

# CRUD для клиентов -- начало
def customer_list(request):
    page_title = 'Список клиентов'
    customers = Customer.objects.all()
    context = {
        'page_title': page_title,
        'customers': customers
    }
    return render(request, 'customers/customer_list.html', context)


# def customer_detail(request, customer_id):

#     customer = Customer.objects.get(id=customer_id)
#     customer_orders = Order.objects.filter(customer=customer)
#     context = {
#         'customer': customer,
#         'customer_orders': customer_orders,
#     }

        
#     return render(request, 'customers/customer_detail.html', context)

def customer_create(request):
    if request.method == 'POST':
        form = CustomerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('customers/customer_list')
    else:
        form = CustomerForm()
    return render(request, 'customers/customer_create.html', {'form': form})

def customer_update(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    if request.method == 'POST':
        form = CustomerForm(request.POST, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customers/customer_list')
    else:
        form = CustomerForm(instance=customer)
    return render(request, 'customers/customer_update.html', {'form': form})

# def customer_delete(request, pk):
#     customer = get_object_or_404(Customer, pk=pk)
#     if request.method == 'POST':
#         customer.delete()
#         return redirect('customers/customer_list')
#     return render(request, 'customers/customer_delete.html', {'customer': customer})

class CustomerDeleteView(DeleteView):
    model = Customer
    template_name = 'customers/customer_delete.html'
    success_url = '/orders/customers/'  # 

# CRUD для клиентов -- конец