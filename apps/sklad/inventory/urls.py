from django.urls import path
from .views.inventory_document_view import inventory_document_view
from .views.generate_pdf_report_view import generate_pdf_report
from .views.generate_excel_view import export_inventory_view
from .admin_site import admin_site


app_name = 'inventory'  # Replace 'your_app' with the actual name of your app

urlpatterns = [
    # path('<path:inventory_id>/inventory/generate-report/', InventoryAdmin.generate_report, name='generate-report'),
    path('inventory/<int:inventory_id>/document/', inventory_document_view, name='inventory-document'),
    path('inventory/<int:inventory_id>/report/', generate_pdf_report, name='inventory-report'),
    path('inventory/export/', export_inventory_view, name='export_inventory'),
]