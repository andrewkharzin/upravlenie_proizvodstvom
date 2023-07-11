from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from import_export import resources
from django.utils.html import format_html
from ..models.employee import Employee, EmplEvent
from ..models.salary import WorkShift
from ..forms import EmployeeForm
from ..utils.shift_excel_report import generate_work_schedule


class EmployeeResource(resources.ModelResource):
    class Meta:
        model = Employee

      
        
class EmployeeAdmin(ImportExportModelAdmin):
    esource_class = EmployeeResource
    form = EmployeeForm
    list_display = ('name', 'position', 'hired_date', 'phone', 'email', 'work_email', 'display_photo', 'rating')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('user')

    def work_email(self, obj):
        if obj.user:
            return obj.user.email
        return "Без доступа"  # Customize the message as needed

    work_email.short_description = 'Доступ к системе'

    def display_photo(self, obj):
        return format_html('<img src="{}" width="50" height="50" />', obj.photo.url)
    display_photo.short_description = 'Фото'

@admin.register(WorkShift)
class WorkShiftAdmin(admin.ModelAdmin):
    actions = [generate_work_schedule]


@admin.register(EmplEvent)
class CalendarEventAdmin(admin.ModelAdmin):
    list_display = ('id', 'event_title', 'event_type', 'event_description')
    list_filter = ('event_type',)
    search_fields = ('event_title',)