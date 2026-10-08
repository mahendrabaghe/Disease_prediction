from pathlib import Path

import numpy as np
import pandas as pd


RNG = np.random.default_rng(42)
ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "sample_patient_data.csv"


FEATURES = [
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


PROFILES = {
    "Heart Disease": {
        "symptoms": {"chest_pain": 0.85, "fatigue": 0.55, "breathing_difficulty": 0.58},
        "age": (52, 11),
        "weight": (78, 12),
        "bp_systolic": (152, 18),
        "bp_diastolic": (94, 10),
        "glucose": (116, 28),
        "oxygen_saturation": (95, 3),
        "history": ["hypertension", "heart disease", "diabetes"],
    },
    "Diabetes": {
        "symptoms": {"fatigue": 0.82, "headache": 0.35, "vomiting": 0.18},
        "age": (48, 12),
        "weight": (82, 14),
        "bp_systolic": (134, 13),
        "bp_diastolic": (86, 8),
        "glucose": (205, 45),
        "history": ["diabetes", "hypertension", "none"],
    },
    "Typhoid": {
        "symptoms": {"fever": 0.95, "headache": 0.72, "vomiting": 0.55, "body_pain": 0.62, "fatigue": 0.7},
        "age": (31, 12),
        "glucose": (92, 13),
        "platelet_count": (175000, 45000),
        "wbc_count": (5200, 1400),
        "typhoid_igg": (1, 0),
        "history": ["none"],
    },
    "Malaria": {
        "symptoms": {"fever": 0.95, "vomiting": 0.5, "body_pain": 0.78, "headache": 0.65, "fatigue": 0.78},
        "age": (34, 14),
        "hemoglobin": (11.2, 1.3),
        "platelet_count": (105000, 35000),
        "bilirubin": (1.15, 0.45),
        "malaria_parasite": (1, 0),
        "history": ["none"],
    },
    "Pneumonia": {
        "symptoms": {"fever": 0.8, "cough": 0.94, "fatigue": 0.65, "breathing_difficulty": 0.88, "chest_pain": 0.35},
        "age": (42, 20),
        "wbc_count": (14500, 3200),
        "oxygen_saturation": (90, 4),
        "history": ["asthma", "none"],
    },
    "Kidney Disease": {
        "symptoms": {"fatigue": 0.75, "vomiting": 0.42, "headache": 0.3, "breathing_difficulty": 0.2},
        "age": (55, 14),
        "bp_systolic": (150, 17),
        "bp_diastolic": (92, 10),
        "creatinine": (2.2, 0.7),
        "hemoglobin": (10.8, 1.4),
        "history": ["kidney disease", "hypertension", "diabetes"],
    },
    "Liver Disease": {
        "symptoms": {"fatigue": 0.72, "vomiting": 0.48, "body_pain": 0.35, "fever": 0.25},
        "age": (46, 13),
        "bilirubin": (2.4, 0.8),
        "alt": (95, 28),
        "ast": (78, 25),
        "history": ["liver disease", "none"],
    },
    "Dengue": {
        "symptoms": {"fever": 0.95, "headache": 0.75, "vomiting": 0.55, "body_pain": 0.88, "fatigue": 0.72},
        "age": (29, 13),
        "hemoglobin": (13.2, 1.4),
        "platelet_count": (65000, 25000),
        "wbc_count": (3600, 1100),
        "history": ["none"],
    },
    "Anemia": {
        "symptoms": {"fatigue": 0.92, "body_pain": 0.42, "headache": 0.38, "breathing_difficulty": 0.25},
        "age": (37, 15),
        "weight": (59, 10),
        "hemoglobin": (8.9, 1.3),
        "platelet_count": (240000, 47000),
        "history": ["anemia", "none"],
    },
}


DEFAULTS = {
    "fever": 0,
    "cough": 0,
    "fatigue": 0,
    "chest_pain": 0,
    "headache": 0,
    "vomiting": 0,
    "body_pain": 0,
    "breathing_difficulty": 0,
    "age": (38, 16),
    "weight": (68, 12),
    "bp_systolic": (120, 12),
    "bp_diastolic": (78, 8),
    "glucose": (96, 15),
    "hemoglobin": (13.8, 1.2),
    "platelet_count": (250000, 52000),
    "wbc_count": (7500, 1700),
    "creatinine": (0.9, 0.18),
    "bilirubin": (0.8, 0.25),
    "alt": (30, 10),
    "ast": (28, 9),
    "oxygen_saturation": (98, 1.5),
    "malaria_parasite": (0, 0),
    "typhoid_igg": (0, 0),
}


def normal(mean, std, min_value=None, max_value=None):
    value = float(RNG.normal(mean, std))
    if min_value is not None:
        value = max(value, min_value)
    if max_value is not None:
        value = min(value, max_value)
    return round(value, 2)


def binary(probability):
    return int(RNG.random() < probability)


def generate_record(disease):
    profile = PROFILES[disease]
    record = {}
    for symptom in [
        "fever",
        "cough",
        "fatigue",
        "chest_pain",
        "headache",
        "vomiting",
        "body_pain",
        "breathing_difficulty",
    ]:
        record[symptom] = binary(profile.get("symptoms", {}).get(symptom, 0.08))

    for key, default in DEFAULTS.items():
        if key in record:
            continue
        mean, std = profile.get(key, default)
        if key in {"malaria_parasite", "typhoid_igg"}:
            record[key] = int(mean)
        elif key in {"age"}:
            record[key] = int(normal(mean, std, 1, 90))
        elif key in {"oxygen_saturation"}:
            record[key] = normal(mean, std, 70, 100)
        elif key in {"platelet_count", "wbc_count"}:
            record[key] = int(normal(mean, std, 1000, 600000))
        else:
            record[key] = normal(mean, std, 0.1, 400)

    record["gender"] = RNG.choice(["female", "male", "other"], p=[0.48, 0.48, 0.04])
    record["medical_history"] = RNG.choice(profile.get("history", ["none"]))
    record["disease"] = disease
    return record


def main():
    rows = []
    for disease in PROFILES:
        for _ in range(130):
            rows.append(generate_record(disease))
    df = pd.DataFrame(rows)
    df = df[FEATURES + ["disease"]]
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(DATA_PATH, index=False)
    print(f"Wrote {len(df)} rows to {DATA_PATH}")


if __name__ == "__main__":
    main()
