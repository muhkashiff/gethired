from datetime import datetime

from app.extensions import db


class Project(db.Model):
    """
    Stores one Resume Optimization project.
    """

    __tablename__ = "projects"

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    project_name = db.Column(
        db.String(200),
        nullable=False
    )

    resume_filename = db.Column(
        db.String(255)
    )

    job_filename = db.Column(
        db.String(255)
    )

    job_text = db.Column(
        db.Text
    )

    ats_score = db.Column(
        db.Float,
        default=0
    )

    optimized_resume = db.Column(
        db.String(255)
    )

    cover_letter = db.Column(
        db.String(255)
    )

    status = db.Column(
        db.String(50),
        default="New"
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    updated_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self):

        return f"<Project {self.project_name}>"