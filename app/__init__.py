from flask import Flask

from app.config import Config

from app.extensions import db
from app.extensions import migrate

from app.dashboard import dashboard_bp


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    migrate.init_app(
        app,
        db
    )

    app.register_blueprint(
        dashboard_bp
    )

    return app