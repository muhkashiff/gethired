"""
Upload Routes
-------------

Handles:
- Resume Upload
- Job Description Upload (future)
"""

from pathlib import Path

from flask import (
    Blueprint,
    current_app,
    flash,
    redirect,
    request,
    url_for,
)

from werkzeug.utils import secure_filename

from app.extensions import db
from app.database import Project

upload_bp = Blueprint(
    "upload",
    __name__,
    url_prefix="/upload"
)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"docx"}


def allowed_file(filename: str) -> bool:
    """
    Check if uploaded file has an allowed extension.
    """
    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS
    )


@upload_bp.route("/resume/<int:project_id>", methods=["POST"])
def upload_resume(project_id):
    """
    Upload a resume for a project.
    """

    project = Project.query.get_or_404(project_id)

    if "resume" not in request.files:
        flash("No file selected.", "danger")
        return redirect(url_for("project.workspace", project_id=project.id))

    file = request.files["resume"]

    if file.filename == "":
        flash("Please choose a DOCX file.", "warning")
        return redirect(url_for("project.workspace", project_id=project.id))

    if not allowed_file(file.filename):
        flash("Only DOCX files are allowed.", "danger")
        return redirect(url_for("project.workspace", project_id=project.id))

    # Create project folder
    upload_folder = (
        Path(current_app.config["UPLOAD_FOLDER"])
        / f"project_{project.id}"
    )

    upload_folder.mkdir(parents=True, exist_ok=True)

    # Save using a standard filename
    filename = "resume_original.docx"

    save_path = upload_folder / filename

    file.save(save_path)

    # Save original filename for display
    project.resume_filename = secure_filename(file.filename)

    project.resume_uploaded = True

    project.status = "Resume Uploaded"

    db.session.commit()

    flash(
        "Resume uploaded successfully.",
        "success",
    )

    return redirect(
        url_for(
            "project.workspace",
            project_id=project.id,
        )
    )