from flask import Blueprint

view_blueprint = Blueprint("view", __name__)

from app.view import routes  # noqa: E402, F401
