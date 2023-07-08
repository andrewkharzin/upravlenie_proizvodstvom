from django import forms
from phonenumber_field.formfields import PhoneNumberField
from apps.employees.models import Employee

class EmployeeForm(forms.ModelForm):
    phone = PhoneNumberField(widget=forms.TextInput(attrs={'placeholder': '+7(XXX)XXX-XX-XX'}))

    class Meta:
        model = Employee
        fields = '__all__'
