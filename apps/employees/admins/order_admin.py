from django.contrib import admin
from ..models.order_outfit import WorkOrderService, WorkOrderStuffIssued
from django.forms.models import BaseInlineFormSet


class WorkOrderStuffIssuedInlineFormset(BaseInlineFormSet):
    def clean(self):
        super().clean()

        for form in self.forms:
            # Получаем выбранное значение поля "employee" из текущей формы
            employee = form.cleaned_data.get('employee')

            # Обновляем значение поля "order_confirmed_preson_name" для текущей формы
            if form.cleaned_data.get('order_confirmed_preson_name') is None:
                form.cleaned_data['order_confirmed_preson_name'] = employee
                form.instance.order_confirmed_preson_name = employee


class WorkOrderStuffIssuedAdminInline(admin.TabularInline):
    formset = WorkOrderStuffIssuedInlineFormset

    class Meta:
        verbose_name = "Выдано/Принято"
    model = WorkOrderStuffIssued
    extra = 1


class WorkOrderServiceInline(admin.TabularInline):

    class Meta:
        verbose_name = "Работы в наряд"
    model = WorkOrderService
    extra = 1


class WorkOrderAdmin(admin.ModelAdmin):
    # Use WorkOrderServiceInline as the inline model
    inlines = [WorkOrderServiceInline, WorkOrderStuffIssuedAdminInline]
    list_display = ('code', 'employee', 'date', 'status')
    list_filter = ('status',)
    search_fields = ('employee__name', 'date')
    actions = ['approve_work_orders']

    delete_confirmation_template = 'admin/delete_confirmation.html'

    raw_id_fields = ['employee']

    def approve_work_orders(self, request, queryset):
        queryset.update(status='APPROVED')
    approve_work_orders.short_description = 'Утвердить выбранные наряды'

    def save_formset(self, request, form, formset, change):
        if formset.model == WorkOrderStuffIssued:
            # Получаем выбранное значение поля "employee"
            employee = form.cleaned_data.get('employee')

            # Обновляем значение поля "order_confirmed_preson_name" для всех связанных объектов "WorkOrderStuffIssued"
            for form in formset.forms:
                if form.cleaned_data.get('order_accept_person_name') is None:
                    form.cleaned_data['order_accept_person_name'] = employee
                    form.instance.order_accept_person_name = employee

        super().save_formset(request, form, formset, change)
