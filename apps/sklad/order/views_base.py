import qrcode
from django.shortcuts import render, get_object_or_404, redirect
from .forms_base import CustomerForm
from django.http import HttpResponse
from io import BytesIO
from .models.order_class import Order
from django.views.generic.edit import DeleteView


from django.shortcuts import render
from .models.customer_class import Customer


# CRUD для клиентов -- начало
def customer_list(request):
    customers = Customer.objects.all()
    return render(request, 'customers/customer_list.html', {'customers': customers})

def customer_detail(request, pk):
    customer = get_object_or_404(Customer, pk=pk)
    return render(request, 'customers/customer_detail.html', {'customer': customer})

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

def generate_qr_code(request, order_id):
    # Получите данные заказа из базы данных или другого источника
    order = Order.objects.get(id=order_id)
    
    # Формируйте текст, который будет закодирован в QR-коде
    data = f"Номер заказа #{order_id}\n\n" \
           f"Клиент: {order.customer}\n" \
           f"Услуги: {order.services}\n" \
           f"Материалы: {order.material}\n" \
           f"Срок оказания: {order.deadline}\n" \
           
    
    # Создайте объект QRCode и сформируйте QR-код из данных
    qr = qrcode.QRCode(version=1, error_correction=qrcode.constants.ERROR_CORRECT_L, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    
    # Создайте изображение QR-кода
    image = qr.make_image(fill_color="blue", back_color="white")
    
    # Создайте HTTP-ответ с изображением QR-кода
    response = HttpResponse(content_type="image/png")
    image.save(response, "PNG")
    
    return response

# def generate_qr_code(request, order_id):
#     # Получение объекта заказа по его идентификатору order_id
#     order = Order.objects.get(id=order_id)
    
#     # Формирование строки с полной информацией о заказе
#     order_info = f"Дата: {order.date}\n"
#     order_info += f"ФИО клиента: {order.customer.name}\n"
#     order_info += "Услуги:\n"
#     for service in order.services.all():
#         order_info += f"- {service.name}, дата оказания: {service.date}, стоимость: {service.cost}\n"
    
#     # Создание объекта QR-кода
#     qr = qrcode.QRCode()
#     qr.add_data(order_info)
#     qr.make(fit=True)
    
#     # Создание изображения QR-кода
#     image = qr.make_image()
    
#     # Создание потока для сохранения изображения
#     qr_code_stream = BytesIO()
#     image.save(qr_code_stream, format='PNG')
#     qr_code_stream.seek(0)
    
#     # Отправка изображения в ответе HTTP
#     response = HttpResponse(content_type='image/png')
#     response.write(qr_code_stream.read())
#     return response