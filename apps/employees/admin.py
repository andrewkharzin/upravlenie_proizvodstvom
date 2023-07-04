from django.contrib import admin
from django.db.models import F, Sum
from django.urls import reverse
from django.utils.html import format_html
from apps.sklad.order.models.service_class import Service
from .models import Employee, WorkShift, Salary, WorkOrder, WorkOrderService, CalendarEvent


@admin.register(Salary)
class SalaryAdmin(admin.ModelAdmin):
    list_display = ('code', 'issued', 'employee', 'date_from', 'date_to', 'total_salary_formatted')
    search_fields = ('employee__name', 'date_from', 'date_to')
    exclude = ('total_salary',)
    
    def total_salary_formatted(self, obj):
        if obj.total_salary == 0:
            return f"К выплате сотруднику {obj.employee} за период {obj.date_from} - {obj.date_to} - Итого: 0"
        return f"К выплате сотруднику {obj.employee} за период {obj.date_from} - {obj.date_to} - Итого: {obj.calculate_total_salary()} " \
               f"Премия за месяц: {obj.bonus} - за вычетом аванса: {obj.advance} - проект:{obj.code}"

    total_salary_formatted.short_description = 'Total Salary'

    def get_total_salary(self, obj):
        return obj.calculate_total_salary()
    get_total_salary.short_description = 'Total Salary'
    get_total_salary.admin_order_field = 'employee'  # Order by employee for consistency

    def get_readonly_fields(self, request, obj=None):
        # Make total_salary read-only
        if obj:
            return self.readonly_fields + ('get_total_salary',)
        return self.readonly_fields

    def save_model(self, request, obj, form, change):
        # Calculate and set total_salary if not already set
        if not obj.total_salary:
            obj.total_salary = obj.calculate_total_salary()
        super().save_model(request, obj, form, change)

class WorkOrderServiceInline(admin.TabularInline):
    model = WorkOrderService
    extra = 1


@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    inlines = [WorkOrderServiceInline]  # Use WorkOrderServiceInline as the inline model
    list_display = ('code','employee', 'date', 'status')
    list_filter = ('status',)
    search_fields = ('employee__name', 'date')
    actions = ['approve_work_orders']
     
    delete_confirmation_template = 'admin/delete_confirmation.html'

    def approve_work_orders(self, request, queryset):
        queryset.update(status='APPROVED')
    approve_work_orders.short_description = 'Утвердить выбранные наряды'




@admin.register(WorkShift)
class WorkShiftAdmin(admin.ModelAdmin):
    list_display = ('employee', 'start_date', 'end_date')
    list_filter = ('employee__name',)
    search_fields = ('employee__name',)

@admin.register(CalendarEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('title', 'event_type', 'start_date', 'end_date')
    list_filter = ('event_type',)
    search_fields = ('title',)


admin.site.register(Employee)



