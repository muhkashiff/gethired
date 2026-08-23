from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    url_for,
)

from app.database import Project


coverletter_bp = Blueprint(
    "coverletter",
    __name__,
    url_prefix="/cover-letter",
)


@coverletter_bp.route(
    "/generate/<int:project_id>",
    methods=["POST"],
)
def generate(project_id):

    project = Project.query.get(project_id)


    if project is None:

        abort(404)


    if not project.resume_uploaded:

        flash(
            "A resume is required before generating a cover letter.",
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
            "A job description is required before generating a cover letter.",
            "danger",
        )

        return redirect(
            url_for(
                "project.workspace",
                project_id=project.id,
            )
        )


    # =====================================================
    # FUTURE COVER LETTER PIPELINE
    # =====================================================
    #
    # resume evidence
    #       +
    # job description
    #       +
    # analysis evidence
    #       ↓
    # advanced linguistic model
    #       ↓
    # natural cover letter
    #       ↓
    # DOCX
    #
    # =====================================================


    flash(
        "Cover letter generation will be connected after the core analysis frontend is complete.",
        "info",
    )


    return redirect(
        url_for(
            "project.workspace",
            project_id=project.id,
        )
    )