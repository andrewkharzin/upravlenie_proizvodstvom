from django.contrib import admin
from PIL import Image
from import_export.admin import ImportExportModelAdmin
from django.contrib import admin
from import_export import resources
from django.contrib.admin import SimpleListFilter
from django.db.models import Count
from django.utils.html import format_html
from .models.materials import Material, MaterialType
from .forms.material_form import MaterialForm


class MaterialResource(resources.ModelResource):
    class Meta:
        model = Material
class MaterialTypeResource(resources.ModelResource):
    class Meta:
        model = MaterialType


class CountryFilter(SimpleListFilter):
    title = 'Country'
    parameter_name = 'country'

    def lookups(self, request, model_admin):
        countries = model_admin.get_queryset(request).order_by(
            'country').values_list('country', 'country')
        return countries.distinct()

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(country=self.value())


# Register your models here.
class MaterialAdmin(ImportExportModelAdmin):
    form = MaterialForm
    resource_class = MaterialResource
    list_display = ['title', 'country', 'color', 'type',
                    'structure', 'density', 'display_image_preview']
    list_filter = ['type', 'structure',]
    search_fields = ['title', 'country',
                     'color', 'type', 'structure', 'density']
    # change_form_template = 'admin/material_change_form.html'

    def display_image_preview(self, obj):
        if obj.image_url:
            return format_html('<img src="{}" width="80" />', obj.image_url.url)
        else:
            return ''

    display_image_preview.short_description = 'Image Preview'


class MaterialTypeAdmin(ImportExportModelAdmin):
    resource_class = MaterialTypeResource
    list_display = ['title',]


admin.site.register(MaterialType, MaterialTypeAdmin)
admin.site.register(Material, MaterialAdmin)
