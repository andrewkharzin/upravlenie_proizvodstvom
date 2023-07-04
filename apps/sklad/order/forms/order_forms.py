from django import forms
from django.forms.widgets import ClearableFileInput, CheckboxSelectMultiple
from ..models.order_class import Order, OrderFile, OrderStuff, OrderService
from apps.sklad.materials.models.material_class import Material
from apps.sklad.order.models.service_class import Service
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Div



class MultipleFileInput(ClearableFileInput):
    """
    A custom widget that allows multiple file uploads.
    """
    template_name = 'widgets/multiple_file_input.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)
        context['widget']['attrs']['multiple'] = True
        return context



class OrderForm(forms.ModelForm):

    # order_type = forms.CharField(widget=forms.Select(attrs={'class': 'form-select mb-2', 'data-control': 'select2', 'data-hide-search': 'true', 'data-placeholder': 'Select an option'}, choices=Order.ORDER_TYPE), label='Тип заказа')
    services = forms.ModelMultipleChoiceField(
        queryset=Service.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

        # exclude = ['materials']  # Exclude any fields you don't want to include in the form

    def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = self.get_default_layout()

    def get_default_layout(self):
        return Layout(
            Field(
                'order_type',
                css_class='form-select mb-2',
                template='orders/widgets/custom_select.html'  # Specify your custom template for select field rendering
            )
            # Add other fields to the layout as needed
        )
    
    class Meta:
        model = Order
        fields = '__all__'

        

class OrderFileForm(forms.ModelForm):
    class Meta:
        model = OrderFile
        fields = ['order_file', 'file_description',]
        widgets = {
            'order_file': MultipleFileInput(),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Field('file', multiple=True),
                'file_description',
            )

class OrderStuffForm(forms.ModelForm):
    class Meta:
        model = OrderStuff
        fields = ['stuff_files', 'stuff_image', 'image_description']
        widgets = {
            'stuff_files': MultipleFileInput(),
            'stuff_image': forms.FileInput(),
        }

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.layout = Layout(
                Field('stuff_files', multiple=True),
                'stuff_image',
                'image_description',
            )


class OrderServiceForm(forms.ModelForm):
    class Meta:
        model = OrderService
        fields = ['service', 'price', 'quantity']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field('service'),
            Field('price'),
            Field('quantity'),
        )

# Crispy Form helper
class CrispyFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.form_tag = False
        self.disable_csrf = True
        self.layout = self.get_layout()

    def get_layout(self):
        return Submit('submit', 'Save')



