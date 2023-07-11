from django.shortcuts import render, get_object_or_404, redirect
from ..models.employee import Employee

def increase_rating(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    employee.rating += 1
    employee.save()
    return redirect('employee/employee_detail', employee_id=employee_id)

def decrease_rating(request, employee_id):
    employee = get_object_or_404(Employee, pk=employee_id)
    if employee.rating > 0:
        employee.rating -= 1
        employee.save()
    return redirect('employee/employee_detail', employee_id=employee_id)
