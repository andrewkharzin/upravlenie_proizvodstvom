from django.shortcuts import render, get_object_or_404
from ..forms.INVDocumentForm import INVDocumentForm
from ..models.inventory import Inventory

def inventory_document_view(request, inventory_id):
    inventory = get_object_or_404(Inventory, id=inventory_id)

    if request.method == 'POST':
        form = INVDocumentForm(request.POST)
        if form.is_valid():
            # Process the form data and save the document
            document_number = form.cleaned_data['number']
            document_date = form.cleaned_data['date']
            # Save the document and associate it with the inventory
            # Example: inventory.document_number = document_number
            #          inventory.document_date = document_date
            #          inventory.save()

            # Redirect to a success page or perform further actions
            return render(request, 'success.html')
    else:
        form = INVDocumentForm()

    return render(request, 'inventory_document.html', {'form': form, 'inventory': inventory})
