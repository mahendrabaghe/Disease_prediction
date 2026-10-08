import re
from pathlib import Path

from werkzeug.utils import secure_filename

from .health_knowledge import DISEASES


ALLOWED_EXTENSIONS = {"pdf", "jpg", "jpeg", "png"}


VALUE_PATTERNS = {
    "glucose": r"(?:glucose|blood sugar|fbs|fasting sugar)\D{0,20}(\d{2,4}(?:\.\d+)?)",
    "hemoglobin": r"(?:hemoglobin|haemoglobin|\bhb\b)\D{0,20}(\d{1,2}(?:\.\d+)?)",
    "platelet_count": r"(?:platelet|plt)\D{0,25}(\d{2,6}(?:,\d{3})?)",
    "wbc_count": r"(?:wbc|white blood cell|leukocyte)\D{0,25}(\d{3,6}(?:,\d{3})?)",
    "creatinine": r"(?:creatinine)\D{0,20}(\d{1,2}(?:\.\d+)?)",
    "bilirubin": r"(?:bilirubin)\D{0,20}(\d{1,2}(?:\.\d+)?)",
    "alt": r"(?:\balt\b|sgpt)\D{0,20}(\d{1,4}(?:\.\d+)?)",
    "ast": r"(?:\bast\b|sgot)\D{0,20}(\d{1,4}(?:\.\d+)?)",
    "oxygen_saturation": r"(?:oxygen saturation|spo2|o2 sat)\D{0,20}(\d{2,3}(?:\.\d+)?)",
}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def save_upload(file_storage, upload_folder):
    filename = secure_filename(file_storage.filename)
    path = Path(upload_folder) / filename
    suffix = path.suffix
    stem = path.stem
    counter = 1
    while path.exists():
        path = Path(upload_folder) / f"{stem}_{counter}{suffix}"
        counter += 1
    file_storage.save(path)
    return path


def extract_text_from_file(path):
    ext = Path(path).suffix.lower()
    if ext == ".pdf":
        return _extract_pdf_text(path)
    if ext in {".jpg", ".jpeg", ".png"}:
        return _extract_image_text(path)
    return ""


def _extract_pdf_text(path):
    try:
        from pypdf import PdfReader
    except ImportError:
        return "PDF text extraction requires pypdf. Install requirements.txt."

    reader = PdfReader(str(path))
    pages = []
    for page in reader.pages:
        pages.append(page.extract_text() or "")
    return "\n".join(pages).strip()


def _extract_image_text(path):
    try:
        from PIL import Image
        import pytesseract
    except ImportError:
        return "Image OCR requires Pillow and pytesseract. Install requirements.txt."

    try:
        return pytesseract.image_to_string(Image.open(path)).strip()
    except Exception as exc:
        return (
            "OCR could not read this image. Check that the Tesseract executable is installed "
            f"and available on PATH. Details: {exc}"
        )


def extract_values(text):
    values = {}
    clean_text = text.lower().replace(",", "")
    for key, pattern in VALUE_PATTERNS.items():
        match = re.search(pattern, clean_text, flags=re.IGNORECASE)
        if match:
            try:
                values[key] = float(match.group(1).replace(",", ""))
            except ValueError:
                continue
    values["malaria_parasite"] = 1 if re.search(r"malaria\D{0,20}(positive|detected)", clean_text) else 0
    values["typhoid_igg"] = 1 if re.search(r"typhoid|widal", clean_text) and re.search(r"positive|reactive", clean_text) else 0
    return values


def detect_abnormalities(values):
    abnormalities = []

    def add(key, label, status, disease, weight):
        abnormalities.append(
            {
                "indicator": key,
                "label": label,
                "status": status,
                "linked_disease": disease,
                "weight": weight,
            }
        )

    glucose = values.get("glucose")
    if glucose is not None and glucose >= 126:
        add("glucose", f"High glucose: {glucose:g} mg/dL", "High", "Diabetes", 30)

    hemoglobin = values.get("hemoglobin")
    if hemoglobin is not None and hemoglobin < 12:
        add("hemoglobin", f"Low hemoglobin: {hemoglobin:g} g/dL", "Low", "Anemia", 30)

    platelets = values.get("platelet_count")
    if platelets is not None and platelets < 150000:
        linked = "Dengue" if platelets < 100000 else "Malaria"
        add("platelet_count", f"Low platelets: {platelets:g} /uL", "Low", linked, 28)

    wbc = values.get("wbc_count")
    if wbc is not None and wbc > 11000:
        add("wbc_count", f"High WBC count: {wbc:g} /uL", "High", "Pneumonia", 18)

    creatinine = values.get("creatinine")
    if creatinine is not None and creatinine > 1.3:
        add("creatinine", f"High creatinine: {creatinine:g} mg/dL", "High", "Kidney Disease", 30)

    bilirubin = values.get("bilirubin")
    if bilirubin is not None and bilirubin > 1.2:
        add("bilirubin", f"High bilirubin: {bilirubin:g} mg/dL", "High", "Liver Disease", 22)

    alt = values.get("alt")
    if alt is not None and alt > 56:
        add("alt", f"High ALT/SGPT: {alt:g} U/L", "High", "Liver Disease", 20)

    ast = values.get("ast")
    if ast is not None and ast > 40:
        add("ast", f"High AST/SGOT: {ast:g} U/L", "High", "Liver Disease", 16)

    oxygen = values.get("oxygen_saturation")
    if oxygen is not None and oxygen < 94:
        add("oxygen_saturation", f"Low oxygen saturation: {oxygen:g}%", "Low", "Pneumonia", 28)

    if values.get("malaria_parasite"):
        add("malaria_parasite", "Malaria parasite detected", "Positive", "Malaria", 45)

    if values.get("typhoid_igg"):
        add("typhoid_igg", "Typhoid/Widal marker appears reactive", "Positive", "Typhoid", 35)

    return abnormalities


def infer_disease(abnormalities):
    if not abnormalities:
        return {
            "predicted_disease": "No high-risk disease pattern detected",
            "risk_percentage": 18,
            "doctor_type": "General Physician",
        }

    scores = {}
    for item in abnormalities:
        disease = item["linked_disease"]
        scores[disease] = scores.get(disease, 0) + item["weight"]
    disease, score = max(scores.items(), key=lambda item: item[1])
    risk = min(95, 30 + score)
    return {
        "predicted_disease": disease,
        "risk_percentage": risk,
        "doctor_type": DISEASES.get(disease, {}).get("doctor_type", "General Physician"),
    }


def analyze_report(path):
    text = extract_text_from_file(path)
    values = extract_values(text)
    abnormalities = detect_abnormalities(values)
    disease_result = infer_disease(abnormalities)
    return {
        "filename": Path(path).name,
        "extracted_text": text,
        "extracted_values": values,
        "abnormalities": abnormalities,
        **disease_result,
    }
