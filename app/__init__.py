from pathlib import Path

from flask import Flask
from flask_login import current_user

from .config import Config
from .extensions import db, login_manager
from .i18n import translate
from .models import User


def create_app(config_class=Config):
    app = Flask(
        __name__,
        instance_relative_config=True,
        template_folder="../templates",
        static_folder="../static",
    )
    app.config.from_object(config_class)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    Path(app.config["UPLOAD_FOLDER"]).mkdir(parents=True, exist_ok=True)
    Path(app.config["MODEL_DIR"]).mkdir(parents=True, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = "auth.login"
    login_manager.login_message_category = "info"

    from .routes.auth import auth_bp
    from .routes.main import main_bp
    from .routes.api import api_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    with app.app_context():
        db.create_all()
        admin_email = app.config["ADMIN_EMAIL"]
        if admin_email and not User.query.filter_by(email=admin_email).first():
            admin = User(name="System Admin", email=admin_email, role="admin")
            admin.set_password(app.config["ADMIN_PASSWORD"])
            db.session.add(admin)
            db.session.commit()

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    @app.context_processor
    def inject_globals():
        return {
            "current_user": current_user,
            "t": translate,
        }

    @app.cli.command("init-db")
    def init_db_command():
        """Create database tables and a demo admin."""
        with app.app_context():
            db.create_all()
            admin_email = app.config["ADMIN_EMAIL"]
            if admin_email and not User.query.filter_by(email=admin_email).first():
                admin = User(
                    name="System Admin",
                    email=admin_email,
                    role="admin",
                )
                admin.set_password(app.config["ADMIN_PASSWORD"])
                db.session.add(admin)
                db.session.commit()
                print(f"Created admin user: {admin_email}")
            print("Database initialized.")

    return app
