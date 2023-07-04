from django.urls import path
from django.contrib.admin import AdminSite
from django.urls import reverse_lazy

class CustomAdminSite(AdminSite):
    site_header = 'Your Site Header'  # Customize the site header text
    site_title = 'Your Site Title'  # Customize the site title text
    index_title = 'Inventory Administration'  # Customize the index page title text

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            path('inventory/export/', self.admin_view(self.export_inventory_view), name='export_inventory'),
        ]
        return my_urls + urls

    def export_inventory_view(self, request):
        # Implement the export_inventory function here
        # This is the same function mentioned in the previous response
        pass

admin_site = CustomAdminSite(name='customadmin')
