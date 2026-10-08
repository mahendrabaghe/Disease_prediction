import json
import sys
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, confusion_matrix
from sklearn.model_selection import cross_val_score, train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier


ROOT = Path(__file__).resolve().parent.parent
DATA_PATH = ROOT / "data" / "sample_patient_data.csv"
MODEL_DIR = ROOT / "models"
MODEL_PATH = MODEL_DIR / "disease_model.joblib"
METRICS_PATH = MODEL_DIR / "training_metrics.json"

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

NUMERIC_COLUMNS = [column for column in FEATURE_COLUMNS if column not in {"gender", "medical_history"}]
CATEGORICAL_COLUMNS = ["gender", "medical_history"]


def ensure_dataset():
    if DATA_PATH.exists():
        return
    sys.path.insert(0, str(ROOT))
    from scripts.generate_sample_data import main as generate

    generate()


def make_preprocessor():
    numeric = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
        ]
    )
    categorical = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            ("encoder", OneHotEncoder(handle_unknown="ignore")),
        ]
    )
    return ColumnTransformer(
        transformers=[
            ("numeric", numeric, NUMERIC_COLUMNS),
            ("categorical", categorical, CATEGORICAL_COLUMNS),
        ]
    )


def candidate_models():
    models = {
        "Random Forest": RandomForestClassifier(n_estimators=240, max_depth=14, random_state=42),
        "Support Vector Machine": SVC(C=2.5, kernel="rbf", probability=True, random_state=42),
        "Decision Tree": DecisionTreeClassifier(max_depth=10, random_state=42),
        "Logistic Regression": LogisticRegression(max_iter=1600),
    }
    try:
        from xgboost import XGBClassifier

        models["XGBoost"] = XGBClassifier(
            n_estimators=160,
            max_depth=5,
            learning_rate=0.08,
            subsample=0.9,
            colsample_bytree=0.9,
            eval_metric="mlogloss",
            random_state=42,
        )
    except Exception:
        pass
    return models


def train():
    ensure_dataset()
    df = pd.read_csv(DATA_PATH)
    x = df[FEATURE_COLUMNS]
    y = df["disease"]
    x_train, x_test, y_train, y_test = train_test_split(
        x,
        y,
        test_size=0.22,
        random_state=42,
        stratify=y,
    )

    results = []
    best_name = None
    best_pipeline = None
    best_accuracy = -1.0
    best_predictions = None

    for name, estimator in candidate_models().items():
        pipeline = Pipeline(
            steps=[
                ("preprocess", make_preprocessor()),
                ("classifier", estimator),
            ]
        )
        pipeline.fit(x_train, y_train)
        predictions = pipeline.predict(x_test)
        accuracy = accuracy_score(y_test, predictions)
        cv_scores = cross_val_score(pipeline, x, y, cv=5, scoring="accuracy")
        results.append(
            {
                "algorithm": name,
                "accuracy": round(float(accuracy), 4),
                "cross_validation_mean": round(float(cv_scores.mean()), 4),
                "cross_validation_std": round(float(cv_scores.std()), 4),
            }
        )
        if accuracy > best_accuracy:
            best_name = name
            best_pipeline = pipeline
            best_accuracy = accuracy
            best_predictions = predictions

    labels = sorted(y.unique())
    matrix = confusion_matrix(y_test, best_predictions, labels=labels)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(best_pipeline, MODEL_PATH)

    metrics = {
        "dataset": str(DATA_PATH.relative_to(ROOT)),
        "rows": int(len(df)),
        "features": FEATURE_COLUMNS,
        "target": "disease",
        "algorithms": results,
        "best_model": best_name,
        "best_accuracy": round(float(best_accuracy), 4),
        "labels": labels,
        "confusion_matrix": matrix.astype(int).tolist(),
        "notes": [
            "Synthetic sample data is provided for education and prototyping.",
            "Replace data/sample_patient_data.csv with clinically validated data before real-world use.",
        ],
    }
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    pd.DataFrame(results).to_csv(MODEL_DIR / "model_comparison.csv", index=False)
    print(f"Best model: {best_name} ({best_accuracy:.3f})")
    print(f"Saved model to {MODEL_PATH}")
    print(f"Saved metrics to {METRICS_PATH}")


if __name__ == "__main__":
    train()
