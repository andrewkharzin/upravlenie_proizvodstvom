from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from ..forms.INVDocumentForm import INVDocumentForm
from ..models.inventory import Inventory

def generate_pdf_report(request, inventory_id):
    # Retrieve the inventory object
    inventory = get_object_or_404(Inventory, id=inventory_id)

    # Retrieve the form data
    form = INVDocumentForm(request.POST or None)

    # Generate the PDF report
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="inventory_report.pdf"'

    p = canvas.Canvas(response)
    p.drawString(100, 750, "Inventory Report")
    p.drawString(100, 700, f"Inventory Name: {inventory.name}")
    # Add more content to the PDF report based on the form data and inventory details
    # Example: p.drawString(x, y, "Field Name: " + form.cleaned_data['field_name'])

    p.showPage()
    p.save()

    return response
