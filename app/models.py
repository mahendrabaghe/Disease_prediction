from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash

from .extensions import db


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(30), default="patient", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    predictions = db.relationship("PredictionHistory", backref="user", lazy=True)
    appointments = db.relationship("Appointment", backref="user", lazy=True)
    reminders = db.relationship("MedicationReminder", backref="user", lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_clinician(self):
        return self.role in {"doctor", "admin"}


class PredictionHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    source = db.Column(db.String(40), default="symptoms", nullable=False)
    disease = db.Column(db.String(100), nullable=False)
    confidence = db.Column(db.Float, nullable=False)
    severity = db.Column(db.String(40), nullable=False)
    doctor_type = db.Column(db.String(120), nullable=False)
    health_score = db.Column(db.Integer, nullable=False)
    inputs_json = db.Column(db.JSON, nullable=False)
    result_json = db.Column(db.JSON, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    doctor_type = db.Column(db.String(120), nullable=False)
    preferred_date = db.Column(db.Date, nullable=False)
    preferred_time = db.Column(db.String(20), nullable=False)
    reason = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(30), default="Requested", nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)


class MedicationReminder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    medicine_name = db.Column(db.String(120), nullable=False)
    dosage = db.Column(db.String(80), nullable=True)
    reminder_time = db.Column(db.String(20), nullable=False)
    note = db.Column(db.String(255), nullable=True)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
