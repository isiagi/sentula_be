from django.http import FileResponse
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.units import inch
from io import BytesIO
from reportlab.lib.styles import getSampleStyleSheet
from datetime import datetime
from saving.models import Saving
from reportlab.lib import colors

def format_currency(value):
    """Format a number as UGX currency."""
    try:
        return f"UGX {value:,.0f}"  # Example: UGX 1,234,567
    except Exception as e:
        return value  # If there's an error, return the value as is

def create_pdf(model_class, user):
    # Retrieve data from the appropriate model
    if user.is_staff:
        data = model_class.objects.all()
    else:
        if model_class == Saving:
            data = model_class.objects.filter(user_id=user)
        else:
            data = model_class.objects.filter(user=user)

    # Handle empty data
    if not data:
        return None

    # Get all fields of the model and filter out fields to exclude
    model_fields = model_class._meta.fields
    exclude_fields = ['id', 'user', 'user_id', 'account_number', 'type', 'saving_id', 'updated_at', 'created_at', 
                      'image_url', 'password', 'otp', 'last_login', 'is_superuser', 'is_active', 'is_staff']

    table_header = [field.verbose_name.title() for field in model_fields if field.name not in exclude_fields]

    # Extract data rows for the table and calculate total for the "amount" field
    total_amount = 0
    table_data = []
    for item in data:
        row = []
        for field in model_fields:
            if field.name not in exclude_fields:
                value = getattr(item, field.name)
                if field.name in ['amount', 'remaining_amount', 'loan_cost'] and value:
                    total_amount += value
                    value = format_currency(value)
                row.append(value)
        table_data.append(row)

    # Create a BytesIO buffer to receive the PDF data
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)

    # Create a list to hold PDF elements
    elements = []

    # Define a style for the heading and normal text
    heading_style = getSampleStyleSheet()["Heading1"]
    normal_style = getSampleStyleSheet()["Normal"]

    # Add a heading
    elements.append(Paragraph(f"ADA Members {model_class.__name__.capitalize()} Report", heading_style))
    elements.append(Spacer(1, 0.5 * inch))

    # Format date fields and wrap long text using Paragraph
    formatted_table_data = []
    for row in table_data:
        formatted_row = []
        for value in row:
            if isinstance(value, datetime):
                formatted_row.append(value.strftime("%Y-%m-%d"))  # Format datetime
            else:
                # Wrap long text using Paragraph
                formatted_row.append(Paragraph(str(value), normal_style))
        formatted_table_data.append(formatted_row)

    # Set column widths
    col_widths = []
    for header in table_header:
        if header == "Granteers" or header == "Remaining Amount" or header == "Date Of Payment" :
            col_widths.append(1.4 * inch)  # Wider column for long text fields
        elif header == "Email Address":
            col_widths.append(2 * inch)  # Smaller column for amount fields
        else:
            col_widths.append(1.1 * inch)  # Default width for other fields

    # Create the table and set table styles
    table = Table([table_header] + formatted_table_data, colWidths=col_widths, repeatRows=1)

    table_style = [
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#77DDBB')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
    ]
    table.setStyle(TableStyle(table_style))
    
    elements.append(table)
    elements.append(Spacer(1, 0.5 * inch))

    # Add total amount at the bottom
    elements.append(Paragraph(f"Total Amount: {format_currency(total_amount)}", normal_style))
    elements.append(Spacer(1, 0.5 * inch))

    # Build the PDF
    doc.build(elements)

    return buffer
