from apps.sklad.inventory.models.utils.excel import export_inventory

def export_inventory_view(request):
    return export_inventory(request)

# def import_inventory(request):
#     if request.method == 'POST':
