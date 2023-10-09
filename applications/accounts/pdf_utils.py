from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import HexColor
from io import BytesIO

def generate_profile_pdf(profile):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(letter), rightMargin=72, leftMargin=72, topMargin=72, bottomMargin=18)
    story = []

    styles = getSampleStyleSheet()
    name_style = ParagraphStyle(
        'nameStyle',
        parent=styles['Heading1'],
        fontSize=32,
        leading=36,
        spaceAfter=12,
        textColor=HexColor('#004f96')
    )
    detail_style = ParagraphStyle(
        'detailStyle',
        parent=styles['BodyText'],
        fontSize=12,
        leading=16,
    )

    # Имя и фамилия
    name = f"{profile.first_name} {profile.last_name}"
    story.append(Paragraph(name, name_style))
    
    # Фотография
    if profile.photo:
        img_path = profile.photo.path
        img = Image(img_path, width=2*inch, height=2*inch)
        img.hAlign = 'RIGHT'
        story.append(img)
        story.append(Spacer(1, 0.5*inch))

    # Дополнительная информация
    story.append(Paragraph(f"Телефон: {profile.telephone}", detail_style))
    story.append(Paragraph(f"Дата рождения: {profile.bday}", detail_style))
    # ... добавьте другие поля профиля ...

    doc.build(story)
    buffer.seek(0)
    return buffer
