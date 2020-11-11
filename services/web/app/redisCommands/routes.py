from flask import jsonify, request, render_template
from app.redisCommands import redis_commands_blueprint  # noqa: E402, F401
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

redis_set_users = "usernames"


# TODO: there should be a secret key necessary to add a user
@redis_commands_blueprint.route("/addUser", methods=["POST"])
def addUser():
    data = request.get_json()
    username = data['username']

    if redis_client.sismember(redis_set_users, username):
        return jsonify({"msg:": "user already exists"}), 409

    redis_client.sadd(redis_set_users, username)

    return jsonify({"msg:": "user added"}), 200
