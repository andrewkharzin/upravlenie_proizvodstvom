from django.urls import reverse
import os
from datetime import datetime
import qrcode
import json
from io import BytesIO
from django.utils import timezone
from django.core.files import File

def generate_qr_code(self):
        # Generate the URL for the order detail page
        url = reverse('admin:order_order_change', args=[self.id])

        # Create the order data dictionary
        order_data = {
            "Номер заказа": self.order_number,
            "Услуга": self.get_order_type_display(),
            "Заказчик": str(self.customer),
            "Срок выполнения": str(self.deadline),
            "Статус": self.order_status
            # Add other fields as needed
        }

        # Convert the order data to a formatted JSON string
        order_data_json = json.dumps(order_data, indent=4)

        # Generate the QR code image
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(order_data_json)
        qr.make(fit=True)
        qr_img = qr.make_image(fill_color="black", back_color="white")

        # Create a BytesIO object to store the QR code image
        qr_code_image = BytesIO()
        qr_img.save(qr_code_image, format='PNG')
        qr_code_image.seek(0)

        # Create a file name for the QR code image
        filename = f'qr_code_{self.order_number}.png'

        # Assign the BytesIO object as the content for the File object
        qr_code_file = File(qr_code_image, filename)

         # Save the QR code image to the field
        self.qr_code_image.save(filename, File(qr_code_image), save=False)
        
        # Return the QR code image path
        return self.qr_code_image.url if self.qr_code_image else None