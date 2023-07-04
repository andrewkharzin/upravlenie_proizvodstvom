
from django import forms
from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from django.db.models import F
from apps.sklad.order.models.order_class import Order, OrderService, OrderStuff, Shipping, Payment
from apps.sklad.order.models.service_class import Service
from apps.sklad.order.models.customer_class import Customer, Passport
from apps.sklad.materials.models.material_class import Material
from django.utils.html import format_html
from apps.sklad.order.models.invoice_class import Invoice
from ..forms_base import OrderStuffFormSet, CustomFileInput
from django.utils.safestring import mark_safe
from django.db import models
from apps.sklad.inventory.models.inventory import InventoryItem
from ..forms_base import OrderCreationForm
from ..forms.order_forms import OrderForm
from mptt.admin import MPTTModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

class MaterialsInline(admin.TabularInline):
    model = Order.materials.through
    extra = 1
    readonly_fields = ['get_stock_quantity']
    classes = ['collapse']

    def get_stock_quantity(self, instance):
        inventory_qty = instance.inventory_item
        inventory_item = InventoryItem.objects.filter(inventory=inventory_qty).first()
        if inventory_item:
            return inventory_item.get_stock_quantity()
        return 'N/A'

    get_stock_quantity.short_description = 'Stock Quantity'


class ShippingInline(admin.StackedInline):
    model = Shipping
    extra = 1
    classes = ['collapse']

class PaymentInline(admin.TabularInline):
    model = Payment
    extra = 1
    readonly_fields = ('amount', 'transaction_id',)

class OrderServiceInline(admin.TabularInline):
    model = OrderService
    extra = 1
    classes = ['collapse']

class OrderStuffInline(admin.TabularInline):
    model = OrderStuff
    formset = OrderStuffFormSet
    fields = ('image_preview', 'stuff_image', 'image_description',)
    classes = ['collapse']

    readonly_fields = ('image_preview',)
    extra = 1
    formfield_overrides = {
        models.ImageField: {'widget': CustomFileInput},
    }

    def image_preview(self, obj):
        if obj.stuff_image:
            return mark_safe('<img src="{}" width="100">'.format(obj.stuff_image.url))
        return None
    image_preview.short_description = 'Image Preview'

# @admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    form = OrderForm
    inlines = [OrderStuffInline, MaterialsInline, OrderServiceInline, ShippingInline, PaymentInline]

    list_display = ['order_number', 'id',  'order_type', 'get_materials', 'customer', 'display_services_total', 'deadline', 'qr_code_thumbnail']
    list_filter = ['order_type']
    search_fields = ['id', 'customer__name']
    autocomplete_fields = ['customer']
    filter_horizontal = ['services']
    readonly_fields = ['display_services_total']

    change_form_template = 'admin/order/order_change_form.html'



    def get_materials(self, obj):
        materials = obj.materials.all()
        return ', '.join(str(material) for material in materials)
    get_materials.short_description = 'Materials'


    def qr_code_thumbnail(self, obj):
        if obj.qr_code_image:
            return format_html('<img src="{}" width="50" height="50" />', obj.qr_code_image.url)
        else:
            return 'No QR Code'

    qr_code_thumbnail.short_description = 'QR Code'

    def change_view(self, request, object_id, form_url='', extra_context=None):
        extra_context = extra_context or {}
        order = self.get_object(request, object_id)
        extra_context['original'] = order
        return super().change_view(request, object_id, form_url, extra_context=extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'material':
            queryset = Material.objects.filter(inventory__items__isnull=False).distinct()
            kwargs['queryset'] = queryset
        return super().formfield_for_foreignkey(db_field, request, **kwargs)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.prefetch_related('services')
    
    def display_services_total(self, obj):
        # Calculate the total services cost for the order
        total = obj.order_services.aggregate(
            total=models.Sum(F('price') * F('quantity'))
        )['total']
        return f"{total or 0} Рублей"  # Add the label "Рубли"

    display_services_total.short_description = 'Итого:'  # Set a descriptive name for the column
    
