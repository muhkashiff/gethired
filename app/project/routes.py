from flask import Blueprint
from flask import redirect
from flask import request
from flask import url_for

from app.extensions import db
from app.models import Project

project_bp = Blueprint(
    "project",
    __name__,
    url_prefix="/project"
)


@project_bp.route("/new", methods=["POST"])
def new_project():

    project_name = request.form.get("gethired")

    if not project_name:

        project_name = "gethired"

    project = Project(
        project_name=project_name
    )

    db.session.add(project)

    db.session.commit()

    return redirect(
        url_for("dashboard.home")
    )