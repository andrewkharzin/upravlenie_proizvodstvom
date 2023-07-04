
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
from .forms_base import OrderStuffFormSet, CustomFileInput
from django.utils.safestring import mark_safe
from django.db import models
from apps.sklad.inventory.models.inventory import InventoryItem
from .forms_base import OrderCreationForm
from .forms.order_forms import OrderForm
from mptt.admin import MPTTModelAdmin
from django_mptt_admin.admin import DjangoMpttAdmin

from .admins.customer_admin import CustomerAdmin
from .admins.order_admin import OrderAdmin 
from .admins.service_admin import ServiceAdmin




@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ('order', 'invoice_number', 'date', 'amount', 'balance_due',)
    list_filter = ('date',)
    search_fields = ('order__customer__name', 'order__customer__id')
    readonly_fields = ('order', 'date', 'amount')
    
@admin.register(OrderService)
class OrderServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'order', 'service', 'quantity', 'price']




admin.site.register(Customer, CustomerAdmin)
admin.site.register(Order, OrderAdmin)
admin.site.register(Service, ServiceAdmin)