from datetime import date
from functools import wraps

from flask import (
    Blueprint,
    current_app,
    flash,
    jsonify,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import current_user, login_required

from ..chatbot import chatbot_reply
from ..email_utils import send_report_email
from ..extensions import db
from ..health_knowledge import DISEASES, GENERAL_DISCLAIMER
from ..ml import load_training_metrics, predict_patient
from ..models import Appointment, MedicationReminder, PredictionHistory, User
from ..pdf_utils import build_prediction_pdf
from ..report_analysis import allowed_file, analyze_report, save_upload


main_bp = Blueprint("main", __name__)


def clinician_required(view):
    @wraps(view)
    @login_required
    def wrapped(*args, **kwargs):
        if not current_user.is_clinician:
            flash("Doctor or admin access is required.", "danger")
            return redirect(url_for("main.dashboard"))
        return view(*args, **kwargs)

    return wrapped


@main_bp.route("/")
def home():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    metrics = load_training_metrics()
    return render_template("home.html", metrics=metrics, disclaimer=GENERAL_DISCLAIMER)


@main_bp.route("/dashboard")
@login_required
def dashboard():
    history = (
        PredictionHistory.query.filter_by(user_id=current_user.id)
        .order_by(PredictionHistory.created_at.desc())
        .limit(8)
        .all()
    )
    reminders = (
        MedicationReminder.query.filter_by(user_id=current_user.id, is_active=True)
        .order_by(MedicationReminder.reminder_time.asc())
        .all()
    )
    appointments = (
        Appointment.query.filter_by(user_id=current_user.id)
        .order_by(Appointment.created_at.desc())
        .limit(5)
        .all()
    )
    labels = [item.created_at.strftime("%b %d") for item in reversed(history)]
    scores = [item.health_score for item in reversed(history)]
    disease_counts = {}
    for item in history:
        disease_counts[item.disease] = disease_counts.get(item.disease, 0) + 1
    latest_score = history[0].health_score if history else 86
    return render_template(
        "dashboard.html",
        history=history,
        reminders=reminders,
        appointments=appointments,
        chart_labels=labels,
        chart_scores=scores,
        disease_counts=disease_counts,
        latest_score=latest_score,
        disclaimer=GENERAL_DISCLAIMER,
    )


@main_bp.route("/predict", methods=["GET", "POST"])
@login_required
def predict():
    if request.method == "POST":
        try:
            result = predict_patient(request.form)
        except FileNotFoundError as exc:
            flash(str(exc), "danger")
            return redirect(url_for("main.training"))
        record = PredictionHistory(
            user_id=current_user.id,
            source="symptoms",
            disease=result["disease"],
            confidence=result["confidence"],
            severity=result["severity"],
            doctor_type=result["doctor_type"],
            health_score=result["health_score"],
            inputs_json=result["features"],
            result_json=result,
        )
        db.session.add(record)
        db.session.commit()
        flash("Prediction complete. Review the guidance and consult a doctor.", "success")
        return redirect(url_for("main.prediction_result", prediction_id=record.id))
    return render_template("predict.html", diseases=DISEASES, disclaimer=GENERAL_DISCLAIMER)


@main_bp.route("/prediction/<int:prediction_id>")
@login_required
def prediction_result(prediction_id):
    prediction = PredictionHistory.query.get_or_404(prediction_id)
    if prediction.user_id != current_user.id and not current_user.is_clinician:
        flash("You do not have access to that report.", "danger")
        return redirect(url_for("main.dashboard"))
    return render_template("result.html", prediction=prediction, disclaimer=GENERAL_DISCLAIMER)


@main_bp.route("/prediction/<int:prediction_id>/download")
@login_required
def download_prediction(prediction_id):
    prediction = PredictionHistory.query.get_or_404(prediction_id)
    if prediction.user_id != current_user.id and not current_user.is_clinician:
        flash("You do not have access to that report.", "danger")
        return redirect(url_for("main.dashboard"))
    path = build_prediction_pdf(prediction)
    return send_file(path, as_attachment=True, download_name="smart_health_report.pdf")


@main_bp.route("/prediction/<int:prediction_id>/email", methods=["POST"])
@login_required
def email_prediction(prediction_id):
    prediction = PredictionHistory.query.get_or_404(prediction_id)
    if prediction.user_id != current_user.id and not current_user.is_clinician:
        flash("You do not have access to that report.", "danger")
        return redirect(url_for("main.dashboard"))
    path = build_prediction_pdf(prediction)
    ok, message = send_report_email(
        request.form.get("email", current_user.email),
        "Your Smart Health Report",
        f"Attached is your AI-assisted health report for {prediction.disease}.\n\n{GENERAL_DISCLAIMER}",
        path,
    )
    flash(message, "success" if ok else "warning")
    return redirect(url_for("main.prediction_result", prediction_id=prediction.id))


@main_bp.route("/reports", methods=["GET", "POST"])
@login_required
def reports():
    analysis = None
    if request.method == "POST":
        uploaded = request.files.get("report")
        if not uploaded or not uploaded.filename:
            flash("Choose a PDF, JPG, or PNG report first.", "warning")
            return redirect(url_for("main.reports"))
        if not allowed_file(uploaded.filename):
            flash("Unsupported file type. Upload PDF, JPG, JPEG, or PNG.", "danger")
            return redirect(url_for("main.reports"))
        path = save_upload(uploaded, current_app.config["UPLOAD_FOLDER"])
        analysis = analyze_report(path)
        disease = analysis["predicted_disease"]
        if disease in DISEASES:
            risk = analysis["risk_percentage"]
            severity = "Critical" if risk >= 85 else "High" if risk >= 65 else "Medium"
            health_score = max(5, 100 - int(risk))
            result_json = {
                "disease": disease,
                "confidence": risk,
                "severity": severity,
                "doctor_type": analysis["doctor_type"],
                "health_score": health_score,
                "recommendations": DISEASES[disease],
                "report_analysis": analysis,
                "top_predictions": [{"disease": disease, "probability": risk}],
            }
            record = PredictionHistory(
                user_id=current_user.id,
                source="report",
                disease=disease,
                confidence=risk,
                severity=severity,
                doctor_type=analysis["doctor_type"],
                health_score=health_score,
                inputs_json=analysis.get("extracted_values", {}),
                result_json=result_json,
            )
            db.session.add(record)
            db.session.commit()
            analysis["prediction_id"] = record.id
        flash("Report analysis complete.", "success")
    return render_template("reports.html", analysis=analysis, disclaimer=GENERAL_DISCLAIMER)


@main_bp.route("/chatbot")
@login_required
def chatbot():
    return render_template("chatbot.html", disclaimer=GENERAL_DISCLAIMER)


@main_bp.route("/chatbot/message", methods=["POST"])
@login_required
def chatbot_message():
    message = request.form.get("message") or (request.json or {}).get("message", "")
    return jsonify({"reply": chatbot_reply(message)})


@main_bp.route("/history")
@login_required
def history():
    records = (
        PredictionHistory.query.filter_by(user_id=current_user.id)
        .order_by(PredictionHistory.created_at.desc())
        .all()
    )
    return render_template("history.html", records=records, disclaimer=GENERAL_DISCLAIMER)


@main_bp.route("/appointments", methods=["GET", "POST"])
@login_required
def appointments():
    if request.method == "POST":
        try:
            preferred_date = date.fromisoformat(request.form.get("preferred_date"))
        except (TypeError, ValueError):
            flash("Choose a valid appointment date.", "warning")
            return redirect(url_for("main.appointments"))
        appointment = Appointment(
            user_id=current_user.id,
            doctor_type=request.form.get("doctor_type", "General Physician"),
            preferred_date=preferred_date,
            preferred_time=request.form.get("preferred_time", "10:00"),
            reason=request.form.get("reason", "Health consultation"),
        )
        db.session.add(appointment)
        db.session.commit()
        flash("Appointment request submitted.", "success")
        return redirect(url_for("main.appointments"))
    items = (
        Appointment.query.filter_by(user_id=current_user.id)
        .order_by(Appointment.created_at.desc())
        .all()
    )
    return render_template("appointments.html", appointments=items, diseases=DISEASES)


@main_bp.route("/reminders", methods=["POST"])
@login_required
def add_reminder():
    reminder = MedicationReminder(
        user_id=current_user.id,
        medicine_name=request.form.get("medicine_name", "").strip() or "Medicine",
        dosage=request.form.get("dosage", "").strip(),
        reminder_time=request.form.get("reminder_time", "09:00"),
        note=request.form.get("note", "").strip(),
    )
    db.session.add(reminder)
    db.session.commit()
    flash("Medicine reminder saved.", "success")
    return redirect(url_for("main.dashboard"))


@main_bp.route("/reminders/<int:reminder_id>/toggle", methods=["POST"])
@login_required
def toggle_reminder(reminder_id):
    reminder = MedicationReminder.query.get_or_404(reminder_id)
    if reminder.user_id != current_user.id:
        flash("You do not have access to that reminder.", "danger")
        return redirect(url_for("main.dashboard"))
    reminder.is_active = not reminder.is_active
    db.session.commit()
    flash("Reminder updated.", "success")
    return redirect(url_for("main.dashboard"))


@main_bp.route("/training")
@login_required
def training():
    return render_template("training.html", metrics=load_training_metrics())


@main_bp.route("/doctor")
@clinician_required
def doctor_panel():
    records = PredictionHistory.query.order_by(PredictionHistory.created_at.desc()).limit(100).all()
    appointments = Appointment.query.order_by(Appointment.created_at.desc()).limit(100).all()
    users = User.query.order_by(User.created_at.desc()).limit(100).all()
    return render_template("doctor_panel.html", records=records, appointments=appointments, users=users)


@main_bp.route("/doctor/appointment/<int:appointment_id>", methods=["POST"])
@clinician_required
def update_appointment(appointment_id):
    appointment = Appointment.query.get_or_404(appointment_id)
    appointment.status = request.form.get("status", appointment.status)
    db.session.commit()
    flash("Appointment status updated.", "success")
    return redirect(url_for("main.doctor_panel"))
