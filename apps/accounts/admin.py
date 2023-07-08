from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User
from django.contrib.auth.models import Group

class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ['email', 'is_staff', 'is_active', 'group_list']
    list_filter = ['is_staff', 'is_active']
    search_fields = ['email']
    ordering = ['email']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    def group_list(self, obj):
        groups = obj.groups.all()
        return ', '.join([group.name for group in groups])

admin.site.register(User, CustomUserAdmin)