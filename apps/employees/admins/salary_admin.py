from django.contrib import admin
from ..utils.shift_excel_report import generate_work_schedule


class SalaryAdmin(admin.ModelAdmin):
    list_display = ('code', 'issued', 'employee', 'date_from',
                    'date_to', 'total_salary_formatted')
    search_fields = ('employee__name', 'date_from', 'date_to')
    exclude = ('total_salary',)

    def total_salary_formatted(self, obj):
        if obj.total_salary == 0:
            return f"К выплате сотруднику {obj.employee} за период {obj.date_from} - {obj.date_to} - Итого: 0"
        return f"К выплате сотруднику {obj.employee} за период {obj.date_from} - {obj.date_to} - Итого к выдаче: {obj.calculate_total_salary()} " \
               f"Премия за месяц: {obj.bonus} - за вычетом аванса: {obj.advance} - проект:{obj.code}"

    total_salary_formatted.short_description = 'Total Salary'

    def get_total_salary(self, obj):
        return obj.calculate_total_salary()
    get_total_salary.short_description = 'Total Salary'
    # Order by employee for consistency
    get_total_salary.admin_order_field = 'employee'

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
