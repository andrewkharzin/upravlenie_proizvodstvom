from django import forms
from django.utils.safestring import mark_safe
from ..models.materials import Material


class MaterialForm(forms.ModelForm):
    larger_image = forms.CharField(label='Larger Image Preview', required=False)

    class Meta:
        model = Material
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        instance = kwargs.get('instance')
        if instance and instance.image_url:
            image_html = f'<img src="{instance.image_url.url}" style="max-width: 500px; max-height: 500px;" />'
            self.fields['larger_image'].widget = forms.widgets.Textarea(attrs={
                                                                        'rows': 5})
            self.fields['larger_image'].help_text = mark_safe(image_html)
