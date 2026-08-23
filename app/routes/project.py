"""
Project Routes
--------------

Handles:

- Project creation
- Project workspace
- Project progress
- Project deletion placeholder
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
from app.database import Project


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

    project_name = request.form.get(
        "project_name",
        ""
    ).strip()


    if not project_name:

        project_name = "Untitled Project"


    project = Project(
        project_name=project_name,
        status="Waiting for Resume",
    )


    db.session.add(project)
    db.session.commit()


    project_folder = (
        Path(current_app.config["UPLOAD_FOLDER"])
        / f"project_{project.id}"
    )


    project_folder.mkdir(
        parents=True,
        exist_ok=True,
    )


    flash(
        "Project created successfully.",
        "success",
    )


    return redirect(
        url_for(
            "project.workspace",
            project_id=project.id,
        )
    )


# -------------------------------------------------------
# Workspace
# -------------------------------------------------------

@project_bp.route("/<int:project_id>")
def workspace(project_id):

    project = Project.query.get(project_id)


    if project is None:

        abort(404)


    progress = calculate_progress(project)


    # Your analysis pipeline should eventually
    # populate this object.

    analysis = getattr(
        project,
        "analysis",
        None,
    )


    return render_template(
        "project.html",

        project=project,

        progress=progress,

        analysis=analysis,
    )


# -------------------------------------------------------
# Delete Project
# -------------------------------------------------------

@project_bp.route(
    "/delete/<int:project_id>",
    methods=["POST"],
)
def delete_project(project_id):

    project = Project.query.get(project_id)


    if project is None:

        abort(404)


    db.session.delete(project)
    db.session.commit()


    flash(
        "Project deleted successfully.",
        "success",
    )


    return redirect(
        url_for("dashboard.home")
    )


# -------------------------------------------------------
# Progress
# -------------------------------------------------------

def calculate_progress(project):
    """
    Frontend pipeline progress.

    Stage 1: Resume uploaded
    Stage 2: Job description uploaded
    Stage 3: Analysis completed
    """

    completed = 0

    if project.resume_uploaded:
        completed += 1

    if project.jd_uploaded:
        completed += 1

    if project.ats_completed:
        completed += 1

    return int((completed / 3) * 100)