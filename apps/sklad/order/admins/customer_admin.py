
from django import forms
from django.contrib import admin
from import_export import resources, fields
from import_export.admin import ImportExportModelAdmin
from django.db.models import F
from apps.sklad.order.models.customer_class import Customer, Passport


class PassportInline(admin.StackedInline):
    model = Passport
    classes = ['collapse']

class CustomerResource(resources.ModelResource):
    passport_number_series = fields.Field(attribute='passport__passport_number_series', column_name='Passport Number Series')
    passport_number = fields.Field(attribute='passport__passport_number', column_name='Passport Number')
    passport_issued_by = fields.Field(attribute='passport__passport_issued_by', column_name='Passport Issued By')
    passport_issue_date = fields.Field(attribute='passport__passport_issue_date', column_name='Passport Issue Date')
    division_code = fields.Field(attribute='passport__division_code', column_name='Division Code')

    class Meta:
        model = Customer
        fields = ('customer_id', 
                  'client_type', 
                  'name', 
                  'city', 
                  'street', 
                  'phone', 
                  'passport_number_series',
                  'passport_number',
                  'division_code')
        import_id_fields = ('client_type', )

# @admin.register(Customer)
class CustomerAdmin(ImportExportModelAdmin):
    resource_class = CustomerResource
    inlines = [PassportInline]
    list_display = ['customer_id', 'client_type', 'name', 'city', 'street', 'phone']
    search_fields = ['name', 'order__order_type']