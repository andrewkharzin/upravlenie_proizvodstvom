from django.contrib import admin
from .models.employee import Employee
from .models.salary import Salary 
from .models.order_outfit import WorkOrder  
from .admins.employee_admin import EmployeeAdmin
from .admins.salary_admin import SalaryAdmin
from .admins.order_admin import WorkOrderAdmin



admin.site.register(Employee, EmployeeAdmin)
admin.site.register(Salary, SalaryAdmin)
admin.site.register(WorkOrder, WorkOrderAdmin)