"""
Project Routes
--------------

Handles:
- Project Workspace
- Open Project
- Rename Project (future)
- Delete Project (future)
"""

from pathlib import Path

from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    current_app,
)

from app.extensions import db
from app.models import Project

project_bp = Blueprint(
    "project",
    __name__,
    url_prefix="/project",
)


# -------------------------------------------------------
# Create Project
# -------------------------------------------------------
@project_bp.route("/new", methods=["POST"])
def new_project():
    """Create a new project."""

    project_name = request.form.get("project_name", "").strip()

    if not project_name:
        project_name = "Untitled Project"

    project = Project(
        project_name=project_name,
        status="Waiting for Resume",
    )

    db.session.add(project)
    db.session.commit()

    # Create project folder
    project_folder = (
        Path(current_app.config["UPLOAD_FOLDER"])
        / f"project_{project.id}"
    )

    project_folder.mkdir(parents=True, exist_ok=True)

    flash("Project created successfully.", "success")

    return redirect(
        url_for(
            "project.workspace",
            project_id=project.id,
        )
    )


# -------------------------------------------------------
# Project Workspace
# -------------------------------------------------------
@project_bp.route("/<int:project_id>")
def workspace(project_id):
    """Open project workspace."""

    project = Project.query.get(project_id)

    if project is None:
        abort(404)

    progress = calculate_progress(project)

    return render_template(
        "project.html",
        project=project,
        progress=progress,
    )


# -------------------------------------------------------
# Delete Project (Future)
# -------------------------------------------------------
@project_bp.route("/delete/<int:project_id>")
def delete_project(project_id):

    flash(
        "Delete functionality will be added later.",
        "info",
    )

    return redirect(
        url_for("dashboard.home")
    )


# -------------------------------------------------------
# Progress Calculator
# -------------------------------------------------------
def calculate_progress(project):
    """
    Calculates overall project completion.
    """

    completed = 0

    if project.resume_uploaded:
        completed += 1

    if project.jd_uploaded:
        completed += 1

    if project.ats_completed:
        completed += 1

    if project.resume_generated:
        completed += 1

    if project.coverletter_generated:
        completed += 1

    return int((completed / 5) * 100)