from django.db import models
from django import forms
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_GET
from django.db.models import F, Sum
from django.forms import inlineformset_factory
from ..models.customer_class import Customer
from ..models.order_class import Order, OrderService, OrderStuff, OrderStuffFile
from ..models.invoice_class import Invoice
from apps.sklad.materials.models.material_class import Material
from django.http import HttpResponse
from django.template.loader import get_template
from django.template import Context
from io import BytesIO
from reportlab.pdfgen import canvas
from django.template.loader import render_to_string
from django.core.exceptions import ObjectDoesNotExist
from ..forms_base import OrderFilterForm
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from ..forms_base import OrderServiceForm, OrderFileForm, OrderStuffForm
from ..forms.order_forms import OrderForm, OrderServiceForm, OrderFileForm, OrderStuffForm


@require_GET
def get_stock_quantity(request):
    material_id = request.GET.get("material_id")
    material = Material.objects.get(id=material_id)
    stock_quantity = material.stock_quantity
    return JsonResponse({"stock_quantity": stock_quantity})


def search_orders(request):
    query = request.GET.get('query')
    orders = Order.objects.filter(order_number__icontains=query)
    return render(request, 'orders/order_list.html', {'orders': orders})

def order_list(request):
    query = request.GET.get('query')
    ORDER_STATUS = (
        ("Заказ принят", "Заказ принят"),
        ("Передано в работу", "Передан в работу"),
        ("Изготовление", "Изготовление"),
        ("Изготовлено", "Изготовлено"),
        ("Работы выполнены", "Работы выполнены")
    )
    if query:
        orders = Order.objects.filter(Q(order_number__icontains=query))
    else:
        orders = Order.objects.all()

    invoice = Invoice.objects.all()
    page_title = 'Список заказов'

    order_status = request.GET.get('order_status')  # Получение значения фильтра из GET-параметра

    if order_status and order_status != 'all':
        orders = orders.filter(order_status=order_status)

    context = {
        'orders': orders,
        'invoice': invoice,
        'page_title': page_title,
        'order_status_choices': ORDER_STATUS
    }
    return render(request, 'orders/order_list.html', context)


def generate_pdf_report(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        invoice = Invoice.objects.get(order=order)
        customer = Customer.objects.get(id=order.customer_id)
        services = order.services.all()
        order_services = OrderService.objects.filter(order=order)
        services_total = order_services.aggregate(
            total=models.Sum(F('price') * F('quantity'))
        )['total']
        services_sub_total = order_services.aggregate(
            total=models.Sum(F('service__initial_cost') * F('quantity'))
        )['total']

        data = {
            'order': order,
            'invoice': invoice,
            'customer': customer,
            'services': services, 
            'order_services': order_services,
            'service_total': services_total,
            'services_sub_total': services_sub_total
        }

        # Получите шаблон
        template = get_template('orders/order_detail.html')
        # Определите контекст данных
        # Отрендерите шаблон с контекстом данных
        rendered_template = template.render({'data': data})


        # Создайте PDF-документ
        pdf_file = BytesIO()
        p = canvas.Canvas(pdf_file)

        # Отрендерите HTML-шаблон в PDF
        p.drawString(100, 100, rendered_template)

        # Завершите создание PDF-документа
        p.showPage()
        p.save()

        # Установите указатель файла на начало
        pdf_file.seek(0)

        # Создайте HTTP-ответ с PDF-файлом
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="orders/order_detail.pdf"'
        response.write(pdf_file.getvalue())

        return response
    except ObjectDoesNotExist:
        return HttpResponse("Order not found.")

def order_detail(request, order_id):
    order = Order.objects.get(id=order_id)
    invoice = Invoice.objects.get(order=order)
    customer = Customer.objects.get(id=order.customer_id)
    services = order.services.all()
    order_services = OrderService.objects.filter(order=order)
    services_total = order_services.aggregate(
        total=models.Sum(F('price') * F('quantity'))
    )['total']
    services_sub_total = order_services.aggregate(
        total=models.Sum(F('service__initial_cost') * F('quantity'))
    )['total']

    context = {
        'order': order,
        'invoice': invoice,
        'customer': customer,
        'services': services, 
        'order_services': order_services,
        'service_total': services_total,
        'services_sub_total': services_sub_total
    }

    return render(request, 'orders/order_detail.html', context)


def create_order(request):
    OrderFileFormSet = inlineformset_factory(OrderStuff, OrderStuffFile, form=OrderFileForm, extra=1)
    # OrderStuffFormSet = inlineformset_factory(Order, Order.stuffs.through, form=OrderStuffForm, extra=1)
    OrderServiceFormSet = inlineformset_factory(Order, Order.services.through, form=OrderServiceForm, extra=1)

    if request.method == 'POST':
        # Handle form submission
        # material_id = request.POST.get('material')
        order_form = OrderForm(request.POST, prefix='order')
        order_service_formset = OrderServiceFormSet(request.POST, prefix='service')
        order_file_formset = OrderFileFormSet(request.POST, request.FILES, prefix='order_file')

        if order_form.is_valid() and order_service_formset.is_valid() and order_file_formset.is_valid():
            # Save the order form
            order = order_form.save()
            materials = order_form.cleaned_data['materials']
            order.materials.set(materials)
            # Save the order service formset
            order_service_formset.instance = order
            order_service_formset.save()

            # Save the order file formset
            order_file_formset.instance = order
            order_file_formset.save()

            # Redirect to success page or do something else
            return redirect('success')

    else:
        # Display the empty forms
        order_form = OrderForm(prefix='order')
        order_service_formset = OrderServiceFormSet(prefix='service')
        order_file_formset = OrderFileFormSet(prefix='order_file')

    context = {
        'order_form': order_form,
        'order_service_formset': order_service_formset,
        'order_file_formset': order_file_formset,
    }

    return render(request, 'orders/create_order.html', context)
# def create_order(request):
#     if request.method == 'POST':
#         form = OrderForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             return redirect('order:order_detail', order_id=order.pk)
#     else:
#         form = OrderForm()
#     return render(request, 'orders/create_order.html', {'form': form})

def update_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('order:order_detail', order_id=order.pk)
    else:
        form = OrderForm(instance=order)
    return render(request, 'update_order.html', {'form': form})

def delete_order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    if request.method == 'POST':
        order.delete()
        return redirect('order:order_list')
    return render(request, 'delete_order.html', {'order': order})
