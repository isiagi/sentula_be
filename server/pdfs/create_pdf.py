from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from saving.models import Saving

def format_currency(value):
    """ Format a number as UGX currency. """
    try:
        # Format value with thousand separators and append 'UGX'
        return f"UGX {value:,.0f}"  # Example: UGX 1,234,567
    except Exception as e:
        return value  # If there's an error, return the value as is


def create_pdf(model_class, user):
    # Retrieve data from the appropriate model
    # if user is not staff get all data else get per user
    if user.is_staff:
        data = model_class.objects.all()
    else:
        if model_class == Saving:
            data = model_class.objects.filter(user_id=user)
        else:
            data = model_class.objects.filter(user=user)

    # handle empty data
    if not data:
        return None
    
    # Get all the fields of the model
    model_fields = model_class._meta.fields
    
    # Extract field names for table header
    table_header = [field.verbose_name.title() for field in model_fields if field.name not in ['id', 'user', 'user_id', 'account_number', 'type', 'saving_id', 'updated_at', 'created_at', 'image_url', 'password', 'otp', 'last_login', 'is_superuser', 'is_active','is_staff']]

    # Extract data rows for the table and calculate total for the "amount" field
    total_amount = 0
    table_data = []
    for item in data:
        row = []
        for field in model_fields:

            if field.name not in ['id', 'user', 'user_id', 'account_number', 'type', 'saving_id', 'updated_at', 'created_at', 'image_url', 'password', 'otp', 'last_login', 'is_superuser', 'is_active', 'is_staff']:

                value = getattr(item, field.name)
                # If the field is "amount", add it to the total
                if field.name == 'amount' or field.name == 'remaining_amount' or field.name == 'loan_cost' and value:
                    total_amount += value
                    # Format the amount as currency
                    value = format_currency(value)
                row.append(value)
        table_data.append(row)

    # Create a BytesIO buffer to receive the PDF data
    buffer = BytesIO()

    # Create the PDF document using ReportLab
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a list to hold PDF elements
    elements = []

    # Define a style for the heading
    heading_style = getSampleStyleSheet()["Heading1"]

    # Define a style for the normal text
    normal_style = getSampleStyleSheet()["Normal"]

    # Add a heading
    elements.append(Paragraph(f"ADA Members {model_class.__name__.capitalize()} Report", heading_style))
    elements.append(Spacer(1, 0.5 * inch))

    # Format date fields in table data
    formatted_table_data = []
    for row in table_data:
        formatted_row = []
        for value in row:
            if isinstance(value, datetime):
                formatted_row.append(value.strftime("%Y-%m-%d"))  # Format datetime to YYYY-MM-DD
            else:
                formatted_row.append(value)
        formatted_table_data.append(formatted_row)

    # Create the table
    table = Table([table_header] + formatted_table_data, repeatRows=1)
    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#77DDBB'),
                              ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('GRID', (0, 0), (-1, -1), 1, '#000000')])
    table.setStyle(table_style)
    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))

    # Add the total amount at the bottom
    elements.append(Paragraph(f"Total Amount: {format_currency(total_amount)}", normal_style))
    elements.append(Spacer(1, 0.5 * inch))

    # Build the PDF document
    doc.build(elements)

    return buffer
