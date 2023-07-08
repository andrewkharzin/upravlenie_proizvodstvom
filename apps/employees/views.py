from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from .models import Employee, WorkShift, Salary, WorkOrder
from apps.sklad.order.models.service_class import Service
from .models import EmplEvent


def calendar_view(request):
    # Получите все события календаря из базы данных
    events = EmplEvent.objects.all()

    # Передайте события в контекст шаблона
    context = {'events': events}

    # Отобразите шаблон calendar.html и передайте контекст
    return render(request, 'employee/calendar.html', context)



def get_price_for_work(request):
    service_id = request.GET.get('service')
    try:
        service = Service.objects.get(id=service_id)
        price_for_work = service.price_for_work
        return JsonResponse({'price_for_work': price_for_work})
    except (Service.DoesNotExist, ValueError):
        return JsonResponse({'price_for_work': None})

def employee_list(request):
    page_title = 'Список сотрудников'
    employees = Employee.objects.all()
    
    employee_data = []
    for employee in employees:
        if employee.user:
            email = employee.user.email
        else:
            email = "No account created"  # Customize the message as needed
        employee_data.append({'employee': employee, 'work_email': email})
    context = {
        'employees': employees,
        'employee_data': employee_data,
        'page_title': page_title
        }
    return render(request, 'employee/list.html', context)

def workshift_list(request):
    workshifts = WorkShift.objects.all()
    return render(request, 'employee/workshift_list.html', {'workshifts': workshifts})

def salary_list(request):
    salaries = Salary.objects.all()
    return render(request, 'employee/salary_list.html', {'salaries': salaries})

def workorder_list(request):
    workorders = WorkOrder.objects.all()
    return render(request, 'employee/workorder_list.html', {'workorders': workorders})



def employee_detail(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    return render(request, 'employee/employee_detail.html', {'employee': employee})

def rate_employee(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if request.method == 'POST':
        rating = float(request.POST.get('rating'))
        employee.rating = rating
        employee.save()
        return redirect('employees:employee_detail', employee_id=employee_id)
    return render(request, 'employee/rate_employee.html', {'employee': employee})