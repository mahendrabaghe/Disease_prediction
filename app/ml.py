import json
import re
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from flask import current_app

from .health_knowledge import DISEASES


SYMPTOM_FIELDS = [
    "fever",
    "cough",
    "fatigue",
    "chest_pain",
    "headache",
    "vomiting",
    "body_pain",
    "breathing_difficulty",
]

FEATURE_COLUMNS = [
    "fever",
    "cough",
    "fatigue",
    "chest_pain",
    "headache",
    "vomiting",
    "body_pain",
    "breathing_difficulty",
    "age",
    "weight",
    "gender",
    "medical_history",
    "bp_systolic",
    "bp_diastolic",
    "glucose",
    "hemoglobin",
    "platelet_count",
    "wbc_count",
    "creatinine",
    "bilirubin",
    "alt",
    "ast",
    "oxygen_saturation",
    "malaria_parasite",
    "typhoid_igg",
]


DEFAULT_VALUES = {
    "age": 35,
    "weight": 68,
    "gender": "other",
    "medical_history": "none",
    "bp_systolic": 120,
    "bp_diastolic": 80,
    "glucose": 95,
    "hemoglobin": 13.8,
    "platelet_count": 250000,
    "wbc_count": 7500,
    "creatinine": 0.9,
    "bilirubin": 0.8,
    "alt": 28,
    "ast": 26,
    "oxygen_saturation": 98,
    "malaria_parasite": 0,
    "typhoid_igg": 0,
}


def _model_path():
    return Path(current_app.config["MODEL_DIR"]) / "disease_model.joblib"


def _metrics_path():
    return Path(current_app.config["MODEL_DIR"]) / "training_metrics.json"


@lru_cache(maxsize=1)
def load_model():
    path = _model_path()
    if not path.exists():
        raise FileNotFoundError(
            f"Model file not found at {path}. Run `python scripts/train_models.py` first."
        )
    return joblib.load(path)


def load_training_metrics():
    path = _metrics_path()
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def _to_bool(value):
    if isinstance(value, bool):
        return int(value)
    if value is None:
        return 0
    return 1 if str(value).strip().lower() in {"1", "true", "yes", "on", "present"} else 0


def _to_float(value, default):
    try:
        if value is None or value == "":
            return default
        return float(str(value).replace(",", "").strip())
    except (TypeError, ValueError):
        return default


def _parse_blood_pressure(value):
    if not value:
        return DEFAULT_VALUES["bp_systolic"], DEFAULT_VALUES["bp_diastolic"]
    match = re.search(r"(\d{2,3})\s*/\s*(\d{2,3})", str(value))
    if match:
        return float(match.group(1)), float(match.group(2))
    systolic = _to_float(value, DEFAULT_VALUES["bp_systolic"])
    return systolic, DEFAULT_VALUES["bp_diastolic"]


def normalize_patient_input(raw):
    data = {}
    for field in SYMPTOM_FIELDS:
        data[field] = _to_bool(raw.get(field))

    bp_systolic, bp_diastolic = _parse_blood_pressure(raw.get("blood_pressure") or raw.get("bp"))
    data.update(
        {
            "age": _to_float(raw.get("age"), DEFAULT_VALUES["age"]),
            "weight": _to_float(raw.get("weight"), DEFAULT_VALUES["weight"]),
            "gender": (raw.get("gender") or DEFAULT_VALUES["gender"]).strip().lower(),
            "medical_history": (raw.get("medical_history") or DEFAULT_VALUES["medical_history"]).strip().lower(),
            "bp_systolic": _to_float(raw.get("bp_systolic"), bp_systolic),
            "bp_diastolic": _to_float(raw.get("bp_diastolic"), bp_diastolic),
            "glucose": _to_float(
                raw.get("sugar_level") or raw.get("glucose"),
                DEFAULT_VALUES["glucose"],
            ),
            "hemoglobin": _to_float(raw.get("hemoglobin"), DEFAULT_VALUES["hemoglobin"]),
            "platelet_count": _to_float(raw.get("platelet_count"), DEFAULT_VALUES["platelet_count"]),
            "wbc_count": _to_float(raw.get("wbc_count"), DEFAULT_VALUES["wbc_count"]),
            "creatinine": _to_float(raw.get("creatinine"), DEFAULT_VALUES["creatinine"]),
            "bilirubin": _to_float(raw.get("bilirubin"), DEFAULT_VALUES["bilirubin"]),
            "alt": _to_float(raw.get("alt"), DEFAULT_VALUES["alt"]),
            "ast": _to_float(raw.get("ast"), DEFAULT_VALUES["ast"]),
            "oxygen_saturation": _to_float(raw.get("oxygen_saturation"), DEFAULT_VALUES["oxygen_saturation"]),
            "malaria_parasite": _to_bool(raw.get("malaria_parasite")),
            "typhoid_igg": _to_bool(raw.get("typhoid_igg")),
        }
    )
    return {column: data.get(column, DEFAULT_VALUES.get(column, 0)) for column in FEATURE_COLUMNS}


def _severity(disease, confidence, features):
    base = DISEASES.get(disease, {}).get("severity_base", "Medium")
    if (
        features.get("oxygen_saturation", 100) < 92
        or features.get("platelet_count", 250000) < 50000
        or features.get("bp_systolic", 120) >= 180
        or features.get("glucose", 95) >= 300
        or features.get("hemoglobin", 13) < 7
    ):
        return "Critical"
    if confidence >= 0.85 and base == "High":
        return "High"
    if confidence < 0.45:
        return "Low"
    return base


def _health_score(severity, confidence):
    severity_penalty = {"Low": 20, "Medium": 38, "High": 58, "Critical": 78}.get(severity, 35)
    score = 100 - severity_penalty - int(max(confidence - 0.5, 0) * 20)
    return int(np.clip(score, 5, 95))


def predict_patient(raw):
    model = load_model()
    features = normalize_patient_input(raw)
    frame = pd.DataFrame([features], columns=FEATURE_COLUMNS)
    probabilities = model.predict_proba(frame)[0]
    classes = list(model.classes_)
    ranked = sorted(zip(classes, probabilities), key=lambda item: item[1], reverse=True)
    disease, probability = ranked[0]
    confidence = round(float(probability) * 100, 2)
    severity = _severity(disease, float(probability), features)
    health_score = _health_score(severity, float(probability))
    knowledge = DISEASES.get(disease, {})

    return {
        "disease": disease,
        "confidence": confidence,
        "severity": severity,
        "doctor_type": knowledge.get("doctor_type", "General Physician"),
        "health_score": health_score,
        "top_predictions": [
            {"disease": name, "probability": round(float(score) * 100, 2)}
            for name, score in ranked[:3]
        ],
        "features": features,
        "recommendations": knowledge,
    }
