from pathlib import Path
from tempfile import NamedTemporaryFile

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

from .health_knowledge import GENERAL_DISCLAIMER


def build_prediction_pdf(prediction):
    result = prediction.result_json
    temp = NamedTemporaryFile(delete=False, suffix=".pdf")
    temp.close()
    path = Path(temp.name)
    pdf = canvas.Canvas(str(path), pagesize=letter)
    width, height = letter
    y = height - 60

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(50, y, "Smart Disease Prediction Health Report")
    y -= 35
    pdf.setFont("Helvetica", 11)
    rows = [
        ("Disease", prediction.disease),
        ("Confidence", f"{prediction.confidence:.2f}%"),
        ("Severity", prediction.severity),
        ("Recommended doctor", prediction.doctor_type),
        ("Health score", str(prediction.health_score)),
        ("Generated", prediction.created_at.strftime("%Y-%m-%d %H:%M")),
    ]
    for label, value in rows:
        pdf.setFont("Helvetica-Bold", 10)
        pdf.drawString(50, y, f"{label}:")
        pdf.setFont("Helvetica", 10)
        pdf.drawString(180, y, str(value))
        y -= 20

    recommendations = result.get("recommendations", {})
    y -= 10
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "General Precautions")
    y -= 18
    pdf.setFont("Helvetica", 9)
    for item in recommendations.get("precautions", []):
        pdf.drawString(65, y, f"- {item}")
        y -= 15

    y -= 8
    pdf.setFont("Helvetica-Bold", 12)
    pdf.drawString(50, y, "Diet Guidance")
    y -= 18
    pdf.setFont("Helvetica", 9)
    pdf.drawString(65, y, f"Foods to eat: {', '.join(recommendations.get('foods_to_eat', []))}")
    y -= 15
    pdf.drawString(65, y, f"Foods to avoid: {', '.join(recommendations.get('foods_to_avoid', []))}")
    y -= 25
    pdf.setFont("Helvetica-Oblique", 8)
    text = pdf.beginText(50, y)
    for line in _wrap(GENERAL_DISCLAIMER, 95):
        text.textLine(line)
    pdf.drawText(text)
    pdf.save()
    return path


def _wrap(text, width):
    words = text.split()
    lines = []
    current = []
    for word in words:
        if len(" ".join(current + [word])) > width:
            lines.append(" ".join(current))
            current = [word]
        else:
            current.append(word)
    if current:
        lines.append(" ".join(current))
    return lines
