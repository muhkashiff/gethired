from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    url_for,
)
from flask import current_app
from app.extensions import db
from app.database import Project


analysis_bp = Blueprint(
    "analysis",
    __name__,
    url_prefix="/analysis",
)


@analysis_bp.route(
    "/run/<int:project_id>",
    methods=["POST"],
)
def run_analysis(project_id):

    project = Project.query.get(project_id)


    if project is None:

        abort(404)


    if not project.resume_uploaded:

        flash(
            "Upload a resume before running analysis.",
            "danger",
        )

        return redirect(
            url_for(
                "project.workspace",
                project_id=project.id,
            )
        )


    if not project.jd_uploaded:

        flash(
            "Upload a job description before running analysis.",
            "danger",
        )

        return redirect(
            url_for(
                "project.workspace",
                project_id=project.id,
            )
        )


    project.status = "Analyzing"

    db.session.commit()


    try:

        # ==================================================
        # CONNECT YOUR EXISTING PIPELINE HERE
        # ==================================================
        #
        # Example conceptual flow:
        #
        # resume_data = resume_pipeline(...)
        #
        # jd_data = jd_pipeline(...)
        #
        # match = knowledge_matching(...)
        #
        # evidence = evidence_enrichment(...)
        #
        # gaps = gap_analysis(...)
        #
        # profile = knowledge_match_profile(...)
        #
        # ats = ats_analysis(...)
        #
        # recommendations = recommendation_engine(...)
        #
        # Store the resulting object/database records.
        #
        # ==================================================


        project.ats_completed = True

        project.status = "Analysis Complete"


        db.session.commit()


        flash(
            "Analysis completed successfully.",
            "success",
        )


    except Exception as exc:

        db.session.rollback()


        project.status = "Analysis Failed"

        db.session.commit()


        current_app.logger.exception(
            "Analysis failed for project %s",
            project.id,
        )


        flash(
            "Analysis failed. Check the application log.",
            "danger",
        )


    return redirect(
        url_for(
            "project.workspace",
            project_id=project.id,
        )
    )