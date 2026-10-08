# Smart Disease Prediction & Health Recommendation System

AI-assisted Flask web application for disease risk prediction, report analysis, health recommendations, dashboards, chatbot guidance, appointments, and model training comparison.

> This system is AI-assisted and not a replacement for professional medical advice. Always consult a certified doctor.

## Supported Diseases

Heart Disease, Diabetes, Typhoid, Malaria, Pneumonia, Kidney Disease, Liver Disease, Dengue, and Anemia.

## Tech Stack

Frontend: HTML, CSS, JavaScript, Bootstrap, Chart.js, Lucide icons  
Backend: Python, Flask, Flask-Login, Flask-SQLAlchemy  
Machine learning: scikit-learn, pandas, NumPy, optional XGBoost  
OCR and NLP: pypdf, pytesseract, regex-based clinical extraction, optional NLTK extension  
Database: SQLite by default, compatible with MySQL/PostgreSQL through `DATABASE_URL`  
Deployment: Gunicorn with Render/Railway/Heroku style configuration

## Complete Folder Structure

```text
app/
  __init__.py
  config.py
  extensions.py
  models.py
  ml.py
  report_analysis.py
  chatbot.py
  health_knowledge.py
  email_utils.py
  pdf_utils.py
  routes/
    auth.py
    main.py
    api.py
templates/
  base.html
  home.html
  dashboard.html
  predict.html
  result.html
  reports.html
  chatbot.html
  history.html
  appointments.html
  training.html
  doctor_panel.html
  auth/
    login.html
    signup.html
static/
  css/style.css
  js/app.js
scripts/
  generate_sample_data.py
  train_models.py
data/
  sample_patient_data.csv
  sample_report.txt
models/
  disease_model.joblib
  training_metrics.json
  model_comparison.csv
docs/
  API_GUIDE.md
  DATABASE_SCHEMA.md
  DEPLOYMENT.md
run.py
wsgi.py
requirements.txt
Procfile
runtime.txt
```

## Main Features

- User signup/login with hashed passwords and patient, doctor, admin roles.
- Patient dashboard with health score, history tracking, charts, reminders, and appointments.
- Symptom and clinical-parameter disease prediction.
- Disease probability, severity, recommended doctor, precautions, general medicine guidance, diet, hydration, exercise, lifestyle, and emergency warnings.
- Medical report upload for PDF, JPG, JPEG, and PNG.
- OCR/PDF extraction and clinical abnormality detection.
- Diet and food recommendation system for each disease.
- AI health assistant chatbot for disease explanations, precautions, diet, emergency signs, and reminder guidance.
- Chart.js visualizations for risk, prediction distribution, health score, model accuracy, and confusion matrix.
- Model training pipeline with missing value handling, encoding, scaling, cross-validation, accuracy comparison, and best-model selection.
- Download health report PDF and email report support.
- Dark/light mode, multi-language navigation labels, responsive UI, and doctor/admin panel.

## Quick Start

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/train_models.py
flask --app run.py init-db
python run.py
```

Open `http://127.0.0.1:5000`.

Demo admin:

```text
Email: admin@example.com
Password: Admin@12345
```

Change these with `ADMIN_EMAIL` and `ADMIN_PASSWORD` in production.

## Model Training

Generate or refresh the sample dataset:

```bash
python scripts/generate_sample_data.py
```

Train and compare models:

```bash
python scripts/train_models.py
```

The script trains:

- Random Forest
- Support Vector Machine
- Decision Tree
- Logistic Regression
- XGBoost if installed

Artifacts:

- `models/disease_model.joblib`
- `models/training_metrics.json`
- `models/model_comparison.csv`

The included dataset is synthetic and intended for education/prototyping. Replace it with clinically validated data before real-world use.

## API Endpoints

- `POST /api/predict`
- `POST /api/report/analyze`
- `POST /api/chat`
- `GET /api/history`
- `GET /api/metrics`
- `GET /api/diseases`

See `docs/API_GUIDE.md` for payload examples.

## Database Schema

The database includes users, prediction history, appointments, and medication reminders. See `docs/DATABASE_SCHEMA.md`.

## Deployment

Use `wsgi.py` and the included `Procfile` for Gunicorn deployments. See `docs/DEPLOYMENT.md`.

## Future Improvements

- Replace synthetic dataset with hospital-approved, anonymized clinical datasets.
- Add calibrated probability thresholds per disease.
- Add doctor verification and role approval workflow.
- Add real SMS/email reminder scheduling with Celery or APScheduler.
- Add multilingual clinical content beyond navigation labels.
- Add DICOM scan analysis with validated imaging models.
- Add FHIR/HL7 integration for hospital systems.
- Add external LLM integration behind a medical safety policy.
