# API Integration Guide

All protected endpoints require an authenticated Flask session. Login through `/login` first, then send requests with the same session cookie.

## Predict Disease

`POST /api/predict`

Content type: `application/json`

```json
{
  "fever": 1,
  "cough": 1,
  "fatigue": 1,
  "chest_pain": 0,
  "blood_pressure": "130/85",
  "sugar_level": 145,
  "age": 42,
  "weight": 74,
  "gender": "male",
  "medical_history": "hypertension",
  "hemoglobin": 13.2,
  "platelet_count": 180000,
  "wbc_count": 12500,
  "oxygen_saturation": 93
}
```

Response:

```json
{
  "disease": "Pneumonia",
  "confidence": 91.24,
  "severity": "High",
  "doctor_type": "Pulmonologist",
  "health_score": 36,
  "top_predictions": []
}
```

## Analyze Report

`POST /api/report/analyze`

Content type: `multipart/form-data`

Field: `report` as PDF, JPG, JPEG, or PNG.

Response includes extracted text, structured values, abnormalities, predicted disease, risk percentage, and doctor type.

## Chat Assistant

`POST /api/chat`

```json
{
  "message": "What should I eat for diabetes?"
}
```

## History

`GET /api/history`

Returns the authenticated user's saved predictions and report analyses.

## Training Metrics

`GET /api/metrics`

Returns algorithm accuracy, cross-validation scores, the best model, labels, and confusion matrix.

## Diseases Knowledge Base

`GET /api/diseases`

Returns diet, precautions, medicine guidance, doctor type, and emergency warnings for supported diseases.
