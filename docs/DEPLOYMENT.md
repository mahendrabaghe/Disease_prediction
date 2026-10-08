# Deployment Instructions

## Local

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python scripts/train_models.py
flask --app run.py init-db
python run.py
```

Open `http://127.0.0.1:5000`.

## Render

1. Push the repository to GitHub.
2. Create a Render Web Service.
3. Set build command:

```bash
pip install -r requirements.txt && python scripts/train_models.py && flask --app run.py init-db
```

4. Set start command:

```bash
gunicorn wsgi:app
```

5. Add environment variables:

```text
SECRET_KEY=<strong-secret>
ADMIN_EMAIL=<admin-email>
ADMIN_PASSWORD=<strong-admin-password>
ADMIN_INVITE_CODE=<private-code>
```

For email reports, also set `MAIL_SERVER`, `MAIL_PORT`, `MAIL_USERNAME`, `MAIL_PASSWORD`, and `MAIL_SENDER`.

## Railway or Heroku

Use the included `Procfile`:

```text
web: gunicorn wsgi:app
```

Run the training script during build or commit the generated `models/disease_model.joblib` and `models/training_metrics.json`.

## OCR Notes

`pytesseract` is the Python wrapper. Image OCR also needs the Tesseract executable installed on the server. PDF text extraction works with embedded text through `pypdf`.
