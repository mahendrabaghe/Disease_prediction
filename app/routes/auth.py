from flask import Blueprint, current_app, flash, redirect, render_template, request, session, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..extensions import db
from ..models import User


auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        role = request.form.get("role", "patient")
        invite_code = request.form.get("invite_code", "").strip()

        if not name or not email or len(password) < 8:
            flash("Enter a name, valid email, and password with at least 8 characters.", "warning")
            return render_template("auth/signup.html")
        if role == "admin" and invite_code != current_app.config["ADMIN_INVITE_CODE"]:
            flash("Admin signup requires a valid invite code.", "danger")
            return render_template("auth/signup.html")
        if role not in {"patient", "doctor", "admin"}:
            role = "patient"
        if User.query.filter_by(email=email).first():
            flash("An account with this email already exists.", "warning")
            return render_template("auth/signup.html")

        user = User(name=name, email=email, role=role)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash("Account created successfully.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("auth/signup.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))
    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("Invalid email or password.", "danger")
            return render_template("auth/login.html")
        login_user(user, remember=bool(request.form.get("remember")))
        flash("Welcome back.", "success")
        return redirect(url_for("main.dashboard"))
    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))


@auth_bp.route("/language/<language>")
def set_language(language):
    if language in {"en", "hi", "es"}:
        session["language"] = language
    return redirect(request.referrer or url_for("main.home"))
