from django.forms.widgets import ClearableFileInput
from django.utils.html import format_html
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

    
class CustomFileInput(ClearableFileInput):
    template_name = 'admin/custom_file_input.html'

    def get_context(self, name, value, attrs):
        context = super().get_context(name, value, attrs)

        download_url = None
        if value and hasattr(value, 'url'):
            download_url = value.url

        context['widget']['download_url'] = download_url

        return context

    def __init__(self, attrs=None):
        default_attrs = {'class': 'custom-file-input'}
        if attrs:
            default_attrs.update(attrs)
        super().__init__(default_attrs)
    
    def get_preview_html(self, value):
        if value and hasattr(value, 'url'):
            return mark_safe(f'<img src="{value.url}" width="100">')
        return ''
    
    def render(self, name, value, attrs=None, renderer=None):
        attrs = attrs or {}
        attrs['class'] = 'custom-file-input'
        preview_html = ''
        if value and hasattr(value, 'url'):
            preview_html = format_html(
                '<img src="{}" width="100" height="100">',
                value.url
        )
        
        download_url = ''
        if value and hasattr(value, 'url'):
                download_url = value.url

        # download_url = value.url if value and hasattr(value, 'url') else ''
        return render_to_string('admin/custom_file_input.html', {
            'name': name,
            'is_hidden': True,
            'required': False,
            'value': value,
            'attrs': attrs,
            'preview_html': preview_html,
            'download_url': download_url,
        })

    # def render(self, name, value, attrs=None, renderer=None):
    #     html = super().render(name, value, attrs, renderer)
    #     download_button = self.get_download_button(value)
    #     return format_html('{}<br>{}', html, download_button)

    def get_download_button(self, value):
        if value:
            return format_html(
                '<a href="{}" class="btn btn-link" download>Download</a>',
                value.url
            )
        else:
            return ''
class CustomClearableFileInput(ClearableFileInput):
    template_name = 'admin/custom_clearable_file_input.html'