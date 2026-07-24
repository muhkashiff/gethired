from flask import Blueprint
from flask import render_template

dashboard_bp = Blueprint(
    "dashboard",
    __name__
)


@dashboard_bp.route("/")
def home():

    from app.database import Project

    projects = Project.query.order_by(
        Project.created_at.desc()
    ).all()

    return render_template(
        "dashboard.html",
        projects=projects
    )