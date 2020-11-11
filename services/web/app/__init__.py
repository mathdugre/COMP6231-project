from flask import Blueprint

web_blueprint = Blueprint("web", __name__)
from . import routes  # noqa: E402, F401

