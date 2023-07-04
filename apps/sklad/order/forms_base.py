from django import forms
from .models.customer_class import Customer
from .models.order_class import Order, OrderStuff, OrderService, OrderFile
# from django.forms import inlineformset_factory, BaseModelFormSet
from django.forms import modelformset_factory, BaseInlineFormSet
from django.utils.safestring import mark_safe
from django.forms.widgets import ClearableFileInput
from .widgets.fileinput_widget import CustomFileInput
from crispy_forms.layout import Layout, Submit, Div, HTML
from crispy_forms.helper import FormHelper
from apps.sklad.materials.models.material_class import Material

class OrderFilterForm(forms.Form):
    order_status = forms.ChoiceField(choices=Order.ORDER_STATUS)

class OrderCreationForm(forms.ModelForm):
    material = forms.ModelChoiceField(queryset=Material.objects.all())
    # Add other fields as needed

    class Meta:
        model = Order
        fields = '__all__'
    
class CustomClearableFileInput(ClearableFileInput):
    def is_hidden(self):
        return False
    # template_name = 'admin/custom_clearable_file_input.html'


class OrderStuffForm(forms.ModelForm):
    stuff_image = forms.ImageField(widget=CustomClearableFileInput)
    class Meta:
        model = OrderStuff
        fields = '__all__'
        widgets = {
            'stuff_image': CustomClearableFileInput,
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stuff_image'].widget.is_hidden = True

    def value_from_datadict(self, data, files, name):
        return files.get(name)
    
    @property
    def get_image_html(self):
        instance = getattr(self.instance, 'stuff_image')
        if instance:
            return mark_safe(
                f'<a href="{instance.url}" target="_blank"><img src="{instance.url}" width="50"></a>'
            )
        return ''

class OrderStuffFormSet(BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for form in self.forms:
            form.empty_permitted = False
            form.fields['stuff_image'].widget.attrs['class'] = 'custom-file-input'
            form.fields['stuff_image'].widget.attrs['id'] = f'id_{form.prefix}-stuff_image'

    
    def add_fields(self, form, index):
        super().add_fields(form, index)
        image_html = self.get_image_html(form.instance.stuff_image)
        form.fields['stuff_image'].widget = CustomFileInput(
            attrs={
                'preview_html': image_html,
                'download_url': self.get_download_url(form.instance.stuff_image),
            }
        )
        

    # def get_image_html(self, name):
    #     return mark_safe(f'<img src="{name.url}" width="100" height="100">')
    
    def get_image_html(self, name):
            if name:
                return mark_safe(f'<img src="{name.url}" width="100" height="100">')
            else:
                return ''
    def get_download_url(self, image):
        if image:
            return image.url
        else:
            return ''
    
    # def get_form_kwargs(self, index):
    #     kwargs = super().get_form_kwargs(index)
    #     kwargs['preview_html'] = self.get_image_html(kwargs['instance'].stuff_image)
    #     return kwargs

    def get_preview_html(self, name):
        if name:
            return self.get_image_html(name)
        else:
            return ''


    @property
    def image_preview(self):
        return mark_safe('<img src="{{ MEDIA_URL }}{}" width="50" height="50">'.format(self.instance.stuff_image))
    
OrderStuffInlineFormSet = forms.inlineformset_factory(
    parent_model=Order,
    model=OrderStuff,
    form=OrderStuffForm,
    formset=OrderStuffFormSet,
    extra=1,
    can_delete=True,
)
class CustomerForm(forms.ModelForm):
    stuff_image = forms.FileField(widget=CustomFileInput, required=False)
    class Meta:
        model = Customer
        fields = ['name', 'city', 'street', 'phone']



class OrderServiceForm(forms.ModelForm):
    class Meta:
        model = OrderService
        fields = '__all__'

class OrderFileForm(forms.ModelForm):
    class Meta:
        model = OrderFile
        fields = '__all__'
