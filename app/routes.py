"""Project workspace and candidate-analysis routes."""

from pathlib import Path

from flask import Blueprint, abort, current_app, flash, redirect, render_template, url_for

from app.extensions import db
from app.database import Project
from app.services.analysis_service import AnalysisPipelineError, CandidateAnalysisService

project_bp = Blueprint("project", __name__, url_prefix="/project")


@project_bp.route("/new", methods=["POST"])
def new_project():
    from flask import request

    project_name = request.form.get("project_name", "").strip()
    if not project_name:
        project_name = "Untitled Project"

    project = Project(
        project_name=project_name,
        status="Waiting for Documents",
    )

    db.session.add(project)
    db.session.commit()

    project_folder = (
        Path(current_app.config["UPLOAD_FOLDER"])
        / f"project_{project.id}"
    )
    project_folder.mkdir(parents=True, exist_ok=True)

    flash("Project created successfully.", "success")
    return redirect(url_for("project.workspace", project_id=project.id))


@project_bp.route("/<int:project_id>")
def workspace(project_id):
    project = Project.query.get_or_404(project_id)

    analysis = CandidateAnalysisService(current_app.config).load(project.id)
    progress = calculate_progress(project)

    return render_template(
        "project.html",
        project=project,
        progress=progress,
        analysis=analysis,
    )


@project_bp.route("/<int:project_id>/analyze", methods=["POST"])
def analyze(project_id):
    project = Project.query.get_or_404(project_id)

    if not project.resume_uploaded or not project.jd_uploaded:
        flash("Upload both the Resume and Job Description before running analysis.", "warning")
        return redirect(url_for("project.workspace", project_id=project.id))

    project.status = "Analysis Running"
    project.ats_completed = False
    db.session.commit()

    try:
        result = CandidateAnalysisService(current_app.config).run(project.id)

        project.ats_score = result["scores"]["ats_compatibility"]
        project.ats_completed = True
        project.status = "Analysis Complete"
        db.session.commit()

        flash("Candidate analysis completed successfully.", "success")

    except AnalysisPipelineError as exc:
        db.session.rollback()
        project = Project.query.get_or_404(project_id)
        project.ats_completed = False
        project.status = "Analysis Failed"
        db.session.commit()
        current_app.logger.exception("Candidate analysis failed: %s", exc)
        flash(f"Analysis could not be completed: {exc}", "danger")

    except Exception as exc:
        db.session.rollback()
        project = Project.query.get_or_404(project_id)
        project.ats_completed = False
        project.status = "Analysis Failed"
        db.session.commit()
        current_app.logger.exception("Unexpected analysis error: %s", exc)
        flash("Analysis failed due to an unexpected error. Check the application log.", "danger")

    return redirect(url_for("project.workspace", project_id=project.id))


@project_bp.route("/delete/<int:project_id>")
def delete_project(project_id):
    flash("Delete functionality will be added later.", "info")
    return redirect(url_for("dashboard.home"))


def calculate_progress(project):
    """Main analysis workflow progress only.

    0   = no documents
    50  = one document
    67  = both documents uploaded / ready to analyze
    100 = analysis complete

    Resume customization and cover letter generation are deliberately not
    counted because they are outside the candidate-analysis pipeline.
    """
    documents = int(bool(project.resume_uploaded)) + int(bool(project.jd_uploaded))

    if project.ats_completed:
        return 100
    if documents == 2:
        return 67
    if documents == 1:
        return 50
    return 0
