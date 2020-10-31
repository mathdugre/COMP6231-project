from flask import Blueprint

jwt_blueprint = Blueprint("jwt", __name__)
from app.jwt import routes  # noqa: E402, F401
