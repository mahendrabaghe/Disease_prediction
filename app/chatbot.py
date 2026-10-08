import re

from .health_knowledge import DISEASES, GENERAL_DISCLAIMER


def _find_disease(message):
    normalized = message.lower()
    for disease in DISEASES:
        if disease.lower() in normalized:
            return disease
    aliases = {
        "heart": "Heart Disease",
        "sugar": "Diabetes",
        "diabetic": "Diabetes",
        "kidney": "Kidney Disease",
        "liver": "Liver Disease",
        "low hb": "Anemia",
        "hemoglobin": "Anemia",
        "platelet": "Dengue",
        "breathing": "Pneumonia",
    }
    for alias, disease in aliases.items():
        if alias in normalized:
            return disease
    return None


def chatbot_reply(message):
    text = (message or "").strip()
    if not text:
        return "Tell me your question or symptom, and I will share general health guidance."

    lower = text.lower()
    disease = _find_disease(lower)

    if any(word in lower for word in ["emergency", "critical", "urgent", "danger"]):
        return (
            "Emergency signs include severe chest pain, severe breathlessness, fainting, confusion, "
            "bleeding, blue lips, seizures, or oxygen below 92 percent. Please seek emergency medical care. "
            + GENERAL_DISCLAIMER
        )

    if "remind" in lower or "reminder" in lower or "medicine" in lower:
        return (
            "I can help you plan reminders: open the Reminders area on the dashboard, add the medicine name, "
            "dosage, and time, and keep following your doctor's prescription. Never change doses without your clinician."
        )

    if disease:
        info = DISEASES[disease]
        if any(word in lower for word in ["diet", "food", "eat", "avoid"]):
            return (
                f"For {disease}, foods to eat include {', '.join(info['foods_to_eat'])}. "
                f"Try to avoid {', '.join(info['foods_to_avoid'])}. {info['diet']} {GENERAL_DISCLAIMER}"
            )
        if any(word in lower for word in ["precaution", "prevent", "care"]):
            return (
                f"Key precautions for {disease}: {', '.join(info['precautions'])}. "
                f"Recommended doctor type: {info['doctor_type']}. {GENERAL_DISCLAIMER}"
            )
        return (
            f"{disease} may require care from a {info['doctor_type']}. "
            f"Basic guidance: {info['diet']} {info['hydration']} "
            f"Emergency warning: {info['emergency']} {GENERAL_DISCLAIMER}"
        )

    symptom_map = [
        (r"chest pain|breathless|shortness of breath", "Chest pain or breathing difficulty can be serious. Please consider urgent medical care, especially if symptoms are severe or sudden."),
        (r"fever.*platelet|platelet.*fever", "Fever with low platelets can occur in dengue or malaria. Get a CBC and medical review quickly."),
        (r"high sugar|glucose", "High glucose can indicate diabetes risk. Confirm with fasting glucose, HbA1c, and a clinician review."),
        (r"low hemoglobin|anaemia|anemia", "Low hemoglobin can suggest anemia. Iron, B12, folate, and bleeding evaluation may be needed."),
    ]
    for pattern, reply in symptom_map:
        if re.search(pattern, lower):
            return f"{reply} {GENERAL_DISCLAIMER}"

    return (
        "I can explain diseases, diet guidance, precautions, report values, emergency signs, and medicine reminder planning. "
        "For a more specific answer, mention a symptom, report value, or disease name. "
        + GENERAL_DISCLAIMER
    )
