from flask import Blueprint, current_app, jsonify, request
from flask_login import current_user, login_required

from ..chatbot import chatbot_reply
from ..extensions import db
from ..health_knowledge import DISEASES
from ..ml import load_training_metrics, predict_patient
from ..models import PredictionHistory
from ..report_analysis import allowed_file, analyze_report, save_upload


api_bp = Blueprint("api", __name__)


@api_bp.route("/predict", methods=["POST"])
@login_required
def api_predict():
    payload = request.get_json(silent=True) or request.form.to_dict()
    result = predict_patient(payload)
    record = PredictionHistory(
        user_id=current_user.id,
        source="api",
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
    result["prediction_id"] = record.id
    return jsonify(result)


@api_bp.route("/report/analyze", methods=["POST"])
@login_required
def api_report_analyze():
    uploaded = request.files.get("report")
    if not uploaded or not uploaded.filename:
        return jsonify({"error": "Missing file field named report."}), 400
    if not allowed_file(uploaded.filename):
        return jsonify({"error": "Unsupported file type."}), 400
    path = save_upload(uploaded, current_app.config["UPLOAD_FOLDER"])
    return jsonify(analyze_report(path))


@api_bp.route("/chat", methods=["POST"])
@login_required
def api_chat():
    payload = request.get_json(silent=True) or {}
    return jsonify({"reply": chatbot_reply(payload.get("message", ""))})


@api_bp.route("/history")
@login_required
def api_history():
    records = (
        PredictionHistory.query.filter_by(user_id=current_user.id)
        .order_by(PredictionHistory.created_at.desc())
        .all()
    )
    return jsonify(
        [
            {
                "id": item.id,
                "source": item.source,
                "disease": item.disease,
                "confidence": item.confidence,
                "severity": item.severity,
                "doctor_type": item.doctor_type,
                "health_score": item.health_score,
                "created_at": item.created_at.isoformat(),
            }
            for item in records
        ]
    )


@api_bp.route("/metrics")
@login_required
def api_metrics():
    return jsonify(load_training_metrics())


@api_bp.route("/diseases")
def api_diseases():
    return jsonify(DISEASES)
