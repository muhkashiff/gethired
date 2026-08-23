"""Document upload routes for a project."""

from pathlib import Path

from flask import Blueprint, current_app, flash, redirect, request, url_for
from werkzeug.utils import secure_filename

from app.extensions import db
from app.database import Project

upload_bp = Blueprint("upload", __name__, url_prefix="/upload")

ALLOWED_EXTENSIONS = {"docx"}


def allowed_file(filename: str) -> bool:
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


def _project_folder(project_id: int) -> Path:
    folder = (
        Path(current_app.config["UPLOAD_FOLDER"])
        / f"project_{project_id}"
    )
    folder.mkdir(parents=True, exist_ok=True)
    return folder


def _reset_analysis(project: Project) -> None:
    """Invalidate stale analysis whenever an input document changes."""
    project.ats_score = 0
    project.ats_completed = False
    project.status = (
        "Ready for Analysis"
        if project.resume_uploaded and project.jd_uploaded
        else "Waiting for Documents"
    )

    output_folder = (
        Path(current_app.config["OUTPUT_FOLDER"])
        / f"project_{project.id}"
    )
    analysis_file = output_folder / "analysis_result.json"
    if analysis_file.exists():
        analysis_file.unlink()


@upload_bp.route("/resume/<int:project_id>", methods=["POST"])
def upload_resume(project_id):
    project = Project.query.get_or_404(project_id)

    if "resume" not in request.files:
        flash("No resume file selected.", "danger")
        return redirect(url_for("project.workspace", project_id=project.id))

    file = request.files["resume"]

    if not file.filename:
        flash("Please choose a DOCX resume.", "warning")
        return redirect(url_for("project.workspace", project_id=project.id))

    if not allowed_file(file.filename):
        flash("Only DOCX files are allowed.", "danger")
        return redirect(url_for("project.workspace", project_id=project.id))

    folder = _project_folder(project.id)
    file.save(folder / "resume_original.docx")

    project.resume_filename = secure_filename(file.filename)
    project.resume_uploaded = True
    _reset_analysis(project)

    db.session.commit()
    flash("Resume uploaded successfully.", "success")

    return redirect(url_for("project.workspace", project_id=project.id))


@upload_bp.route("/jd/<int:project_id>", methods=["POST"])
def upload_jd(project_id):
    project = Project.query.get_or_404(project_id)

    if "jd" not in request.files:
        flash("No Job Description file selected.", "danger")
        return redirect(url_for("project.workspace", project_id=project.id))

    file = request.files["jd"]

    if not file.filename:
        flash("Please choose a DOCX Job Description.", "warning")
        return redirect(url_for("project.workspace", project_id=project.id))

    if not allowed_file(file.filename):
        flash("Only DOCX files are allowed.", "danger")
        return redirect(url_for("project.workspace", project_id=project.id))

    folder = _project_folder(project.id)
    file.save(folder / "job_description_original.docx")

    project.job_filename = secure_filename(file.filename)
    project.jd_uploaded = True
    _reset_analysis(project)

    db.session.commit()
    flash("Job Description uploaded successfully.", "success")

    return redirect(url_for("project.workspace", project_id=project.id))
