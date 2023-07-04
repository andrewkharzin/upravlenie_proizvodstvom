from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from ..models.invoice_class import Invoice


def generate_invoice_report(invoice):
    # Create a BytesIO buffer to store the PDF
    buffer = BytesIO()

    # Define the document title and page size
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = []

    # Define the styles for the report
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading1']
    normal_style = styles['Normal']

    # Add the title to the report
    elements.append(Paragraph('Invoice Report', title_style))
    elements.append(Spacer(1, 24))

    # Add the invoice details to the report
    elements.append(Paragraph(f'Invoice Number: {invoice.number}', heading_style))
    elements.append(Paragraph(f'Customer: {invoice.customer}', normal_style))
    elements.append(Spacer(1, 12))

    # Add the invoice table to the report
    data = [
        ['Description', 'Quantity', 'Price', 'Total'],
        # Add rows for each invoice item
        # Example: ['Item 1', 2, 10.0, 20.0],
        #          ['Item 2', 3, 15.0, 45.0],
    ]
    table_style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.black),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (-1, -1), (-2, -2), 'RIGHT'),
        ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, -1), (-1, -1), 12),
        ('BACKGROUND', (-1, -1), (-1, -1), colors.lightblue),
        ('TEXTCOLOR', (-1, -1), (-1, -1), colors.black),
        ('ALIGN', (-1, -1), (-1, -1), 'CENTER'),
    ])
    table = Table(data, style=table_style)
    elements.append(table)
    elements.append(Spacer(1, 24))

    # Add the invoice summary to the report
    elements.append(Paragraph(f'Total Amount: {invoice.amount}', normal_style))
    elements.append(Paragraph(f'Advance Payment: {invoice.advance_payment}', normal_style))
    elements.append(Paragraph(f'Balance Due: {invoice.balance_due}', normal_style))

    # Build the report
    doc.build(elements)

    # Get the PDF content from the buffer
    pdf = buffer.getvalue()
    buffer.close()

    return pdf_content = generate_invoice_report(invoice)

# Save the PDF to a file
with open('invoice_report.pdf', 'wb') as f:
    f.write(pdf_content)

