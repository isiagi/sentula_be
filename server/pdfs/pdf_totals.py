from django.http import FileResponse
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO
from saving.models import Saving
from loan.models import Loan
from payment.models import Payment
from wagubumbuzi.models import Wagubumbuzi
from userauth.models import CustomUser


def format_currency(value):
    """ Format a number as UGX currency. """
    try:
        # Format value with thousand separators and append 'UGX'
        return f"UGX {value:,.0f}"  # Example: UGX 1,234,567
    except Exception as e:
        return value  # If there's an error, return the value as is
    

def get_user_totals(user):
    total_saving = sum(item.amount for item in Saving.objects.filter(user_id=user) if item.amount)
    total_loan = sum(item.amount for item in Loan.objects.filter(user=user) if item.amount)
    total_payment = sum(item.amount for item in Payment.objects.filter(user=user) if item.amount)
    total_wagubumbuzi = sum(item.amount for item in Wagubumbuzi.objects.filter(user=user) if item.amount)
    
    return {
        'first_name': user.first_name,
        'last_name': user.last_name,
        'total_saving': total_saving,
        'total_loan': total_loan,
        'total_payment': total_payment,
        'total_wagubumbuzi': total_wagubumbuzi
    }

def create_staff_totals_pdf():
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    elements = []

    heading_style = getSampleStyleSheet()["Heading1"]
    normal_style = getSampleStyleSheet()["Normal"]

    # Add heading for the PDF
    elements.append(Paragraph("ADA Members Totals Report", heading_style))
    elements.append(Spacer(1, 0.5 * inch))

    # Table header
    table_header = ['Username', 'First Name', 'Last Name', 'Total Saving', 'Total Loan', 'Total Payment', 'Total Wagubumbuzi']

    # Fetch all users
    users = CustomUser.objects.all()

    print(users, 'usersz')

    # Populate table rows with username and totals
    table_data = [table_header]
    for user in users:
        print(user, 'testing')
        if isinstance(user, CustomUser) and user.is_superuser:
            continue
        print(f"Processing user: {user.username}")
        user_totals = get_user_totals(user)
        print(user_totals, 'user_totals')
        print(f"Totals for {user.username}: {user_totals}")
        formatted_row = [
            user.username,  # Username
            user.first_name,                 # First Name
            user.last_name,                  # Last Name
            format_currency(user_totals['total_saving']),  # Total Saving
            format_currency(user_totals['total_loan']),  # Total Loan
            format_currency(user_totals['total_payment']),  # Total Payment
            format_currency(user_totals['total_wagubumbuzi'])   # Total Wagubumbuzi
        ]
        table_data.append(formatted_row)

    # Create the table
    table = Table(table_data, repeatRows=1)
    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), '#77DDBB'),
                              ('TEXTCOLOR', (0, 0), (-1, 0), '#000000'),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('GRID', (0, 0), (-1, -1), 1, '#000000')])
    table.setStyle(table_style)
    elements.append(table)

    # Build the PDF
    doc.build(elements)
    return buffer