from werkzeug.security import check_password_hash
from flask import jsonify, request, render_template, redirect, make_response
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

from app.models import User
from app.jwt import jwt_blueprint


@jwt_blueprint.route("/")
def index():
    return render_template("index.html")


@jwt_blueprint.route("/auth/login", methods=["POST"])
def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({"msg": "Missing credentials for login!"}), 401

    username = auth.username.lower()
    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"msg": "Provided username does not exist!"}), 401

    if check_password_hash(user.password, auth.password):
        identity = {
            "public_id": user.public_id,
            "username": username,
            "admin": user.admin,
        }
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        resp = jsonify({"login": True})
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp

    else:
        return jsonify({"msg": "Invalid login information!"}), 401


@jwt_blueprint.route("/auth/loginFrontEnd", methods=["POST"])
def loginFrontEnd():
    username = request.form['username']
    password = request.form['password']

    user = User.query.filter_by(username=username).first()

    if not user:
        return jsonify({"msg": "Provided username does not exist!"}), 401

    if check_password_hash(user.password, password):
        identity = {
            "public_id": user.public_id,
            "username": username,
            "admin": user.admin,
        }
        access_token = create_access_token(identity=identity)
        refresh_token = create_refresh_token(identity=identity)

        url_root = request.url_root.split(':')
        url_redir = url_root[0] + ':' + url_root[1] + ':' + str(5005)

        resp = make_response(redirect(url_redir, 301))
        set_access_cookies(resp, access_token)
        set_refresh_cookies(resp, refresh_token)
        return resp

    else:
        return jsonify({"msg": "Invalid login information!"}), 401


@jwt_blueprint.route("/auth/refresh", methods=["POST"])
@jwt_refresh_token_required
def refresh():
    current_user = get_jwt_identity()
    access_token = create_access_token(identity=current_user)

    resp = jsonify({"refresh": True})
    set_access_cookies(resp, access_token)
    return resp, 200


@jwt_blueprint.route("/auth/logout", methods=["POST"])
def logout():

    url_root = request.url_root.split(':')
    url_redir = url_root[0] + ':' + url_root[1] + ':' + str(5000)

    resp = make_response(redirect(url_redir, 301))
    unset_jwt_cookies(resp)
    return resp, 301


@jwt_blueprint.route("/api/whoami", methods=["GET"])
@jwt_required
def whoami():
    current_user = get_jwt_identity()
    return jsonify(current_user), 200
