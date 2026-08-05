import os
import secrets
from pathlib import Path

from flask import Flask

from app.database import init_app as init_database_app
from app.database import initialize_database
from app.routes.auth import auth_bp
from app.routes.equipment import equipment_bp
from app.security import csrf_token


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("LABTRACK_SECRET_KEY") or secrets.token_hex(32),
        DATABASE=str(Path(app.instance_path) / "inventario.sqlite3"),
        ADMIN_USERNAME=os.environ.get("LABTRACK_ADMIN_USER", "admin"),
        ADMIN_PASSWORD=os.environ.get("LABTRACK_ADMIN_PASSWORD"),
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)
    init_database_app(app)
    app.jinja_env.globals["csrf_token"] = csrf_token
    app.register_blueprint(auth_bp)
    app.register_blueprint(equipment_bp)

    with app.app_context():
        initialize_database()

    return app
