"""
Upload Routes
-------------

Handles:
- Resume Upload
- Job Description Upload

Step 1:
Only handles document ingestion.
The analysis pipeline is NOT automatically executed.
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
    url_prefix="/upload",
)


# -------------------------------------------------------
# Allowed file extensions
# -------------------------------------------------------

ALLOWED_RESUME_EXTENSIONS = {"docx"}

ALLOWED_JD_EXTENSIONS = {"docx", "pdf", "txt"}


def allowed_file(filename: str, allowed_extensions: set[str]) -> bool:
    """Check whether a filename has an allowed extension."""

    return (
        "." in filename
        and filename.rsplit(".", 1)[1].lower()
        in allowed_extensions
    )


# -------------------------------------------------------
# Project upload folder
# -------------------------------------------------------

def get_project_upload_folder(project_id: int) -> Path:
    """Return and create the project's upload directory."""

    folder = (
        Path(current_app.config["UPLOAD_FOLDER"])
        / f"project_{project_id}"
    )

    folder.mkdir(
        parents=True,
        exist_ok=True,
    )

    return folder


# -------------------------------------------------------
# Resume Upload
# -------------------------------------------------------

@upload_bp.route(
    "/resume/<int:project_id>",
    methods=["POST"],
)
def upload_resume(project_id):
    """Upload the candidate resume."""

    project = Project.query.get_or_404(project_id)

    if "resume" not in request.files:
        flash(
            "No resume file was selected.",
            "danger",
        )

        return redirect(
            url_for(
                "project.workspace",
                project_id=project.id,
            )
        )

    file = request.files["resume"]

    if not file.filename:
        flash(
            "Please choose a resume file.",
            "warning",
        )

        return redirect(
            url_for(
                "project.workspace",
                project_id=project.id,
            )
        )

    if not allowed_file(
        file.filename,
        ALLOWED_RESUME_EXTENSIONS,
    ):
        flash(
            "Only DOCX resume files are allowed.",
            "danger",
        )

        return redirect(
            url_for(
                "project.workspace",
                project_id=project.id,
            )
        )

    upload_folder = get_project_upload_folder(
        project.id
    )

    # Keep a predictable internal filename.
    filename = "resume_original.docx"

    save_path = upload_folder / filename

    file.save(save_path)

    project.resume_filename = secure_filename(
        file.filename
    )

    project.resume_uploaded = True

    # Do not run analysis here.
    if project.jd_uploaded:
        project.status = "Ready for Analysis"
    else:
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


# -------------------------------------------------------
# Job Description Upload
# -------------------------------------------------------

@upload_bp.route(
    "/jd/<int:project_id>",
    methods=["POST"],
)
def upload_jd(project_id):
    """Upload the job description."""

    project = Project.query.get_or_404(project_id)

    if "jd" not in request.files:
        flash(
            "No job description file was selected.",
            "danger",
        )

        return redirect(
            url_for(
                "project.workspace",
                project_id=project.id,
            )
        )

    file = request.files["jd"]

    if not file.filename:
        flash(
            "Please choose a job description file.",
            "warning",
        )

        return redirect(
            url_for(
                "project.workspace",
                project_id=project.id,
            )
        )

    if not allowed_file(
        file.filename,
        ALLOWED_JD_EXTENSIONS,
    ):
        flash(
            "Allowed job description formats are DOCX, PDF, or TXT.",
            "danger",
        )

        return redirect(
            url_for(
                "project.workspace",
                project_id=project.id,
            )
        )

    upload_folder = get_project_upload_folder(
        project.id
    )

    extension = file.filename.rsplit(
        ".",
        1,
    )[1].lower()

    filename = f"jd_original.{extension}"

    save_path = upload_folder / filename

    file.save(save_path)

    project.job_filename = secure_filename(
        file.filename
    )

    project.jd_uploaded = True

    if project.resume_uploaded:
        project.status = "Ready for Analysis"
    else:
        project.status = "JD Uploaded"

    db.session.commit()

    flash(
        "Job description uploaded successfully.",
        "success",
    )

    return redirect(
        url_for(
            "project.workspace",
            project_id=project.id,
        )
    )