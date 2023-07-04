from django.shortcuts import render
from django.http import JsonResponse
from .models import Employee, WorkShift, Salary, WorkOrder
from apps.sklad.order.models.service_class import Service
from .models import CalendarEvent


def calendar_view(request):
    # Получите все события календаря из базы данных
    events = CalendarEvent.objects.all()

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
    employees = Employee.objects.all()
    return render(request, 'employees/employee_list.html', {'employees': employees})

def workshift_list(request):
    workshifts = WorkShift.objects.all()
    return render(request, 'employees/workshift_list.html', {'workshifts': workshifts})

def salary_list(request):
    salaries = Salary.objects.all()
    return render(request, 'employees/salary_list.html', {'salaries': salaries})

def workorder_list(request):
    workorders = WorkOrder.objects.all()
    return render(request, 'employees/workorder_list.html', {'workorders': workorders})
