from flask import Flask

from app.config import Config
from app.extensions import db, migrate

# Import Models
from app.database import Project

# Import Blueprints
from app.dashboard import dashboard_bp
from app.project import project_bp
from app.upload import upload_bp
from app.routes.analysis import analysis_bp
from app.routes.coverletter import coverletter_bp



def create_app():
    """
    Application Factory
    """

    app = Flask(__name__)

    # Load Configuration
    app.config.from_object(Config)

    # Initialize Extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(project_bp)
    app.register_blueprint(upload_bp)
    app.register_blueprint(analysis_bp)
    app.register_blueprint(coverletter_bp)
    
    # Create database tables (temporary for development)
    with app.app_context():
        db.create_all()

    return app

#"""Application services."""

#from .analysis_service import AnalysisPipelineError, CandidateAnalysisService

#__all__ = ["AnalysisPipelineError", "CandidateAnalysisService"]
