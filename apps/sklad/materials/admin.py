# inventory/admin.py
from django.utils.html import format_html
from django.contrib import admin
from django.contrib.contenttypes.admin import GenericTabularInline
from .models.material_class import Material, MaterialType, Property

class PropertyInline(GenericTabularInline):
    model = Property
    extra = 1

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):

    

    inlines = [PropertyInline]
    list_display = ['name', 'material_type', 'display_related_objects', 'display_image']
    # display_related_objects.short_description = 'Характеристики'
    readonly_fields = ['display_image']
    search_fields = ['name', 'material_type']

    actions = ['duplicate_selected']

    def duplicate_selected(self, request, queryset):
        for obj in queryset:
            obj.pk = None  # Сбрасываем первичный ключ
            obj.save()     # Сохраняем объект с новым первичным ключом

    duplicate_selected.short_description = "Дублировать выбранные записи"
    
    
    def display_image(self, obj):
        if obj.image:
            return format_html('<img src="{}" alt="{}" style="max-height: 200px;">', obj.image.url, obj.name)
        else:
            return 'No image available'

    display_image.short_description = 'Image Preview'
    display_image.allow_tags = True

    def display_related_objects(self, obj):
        related_objects = obj.properties.all()
        return ', '.join(str(related_object) for related_object in related_objects)

# admin.site.register(Material, MaterialAdmin)
admin.site.register(MaterialType)
