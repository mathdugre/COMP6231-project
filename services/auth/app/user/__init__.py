from flask import Blueprint

user_blueprint = Blueprint("user", __name__)
from app.user import routes  # noqa: E402, F401
