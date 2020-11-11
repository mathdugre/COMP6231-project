from flask import jsonify, request, render_template
from app.view import view_blueprint  # noqa: E402, F401
from flask_jwt_extended import (
    create_access_token,
    jwt_required,
    jwt_refresh_token_required,
    create_refresh_token,
    get_jwt_identity,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
)
from app import redis_client


@view_blueprint.route("/", methods=["GET"])
@jwt_required
def mainPage():
    username = get_jwt_identity()['username']
    return render_template("main.html", user_display_name=username)
