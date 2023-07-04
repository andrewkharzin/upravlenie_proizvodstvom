from django.http import JsonResponse
from .models.material_class import Material

def material_info(request):
    material_id = request.GET.get('material_id')
    material = Material.objects.filter(id=material_id).first()
    data = {
        'quantity': material.inventory.quantity if material else None,
    }
    return JsonResponse(data)
