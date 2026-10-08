import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent.parent


class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-this-secret")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL",
        f"sqlite:///{BASE_DIR / 'instance' / 'smart_health.db'}",
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.environ.get("UPLOAD_FOLDER", str(BASE_DIR / "uploads"))
    MODEL_DIR = os.environ.get("MODEL_DIR", str(BASE_DIR / "models"))
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@example.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "Admin@12345")
    ADMIN_INVITE_CODE = os.environ.get("ADMIN_INVITE_CODE", "SMART-ADMIN")
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "")
    MAIL_PORT = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "")
    MAIL_SENDER = os.environ.get("MAIL_SENDER", MAIL_USERNAME)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", "true").lower() == "true"
