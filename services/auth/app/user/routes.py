from functools import wraps
import uuid
import requests

from flask import jsonify, request
from flask_jwt_extended.utils import get_jwt_identity
from flask_jwt_extended.view_decorators import jwt_required
from werkzeug.security import generate_password_hash

from app import db
from app.models import User
from app.user import user_blueprint


def _get_user_info(user):
    return {
        "public_id": user.public_id,
        "username": user.username,
        "email": user.email,
        "admin": user.admin,
    }


def admin_only(f):
    @wraps(f)
    @jwt_required
    def wrapper(*args, **kwargs):
        current_user = get_jwt_identity()

        if not current_user or not current_user["admin"]:
            return jsonify({"msg": "Access denied!"}), 403
        else:
            return f(*args, **kwargs)

    return wrapper


@user_blueprint.route("/user", methods=["GET"])
@admin_only
def get_all_users():
    users = User.query.all()

    return jsonify({"users": [_get_user_info(user) for user in users]})


@user_blueprint.route("/user/<public_id>", methods=["GET"])
@admin_only
def get_one_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"msg": "User not found!"})

    return jsonify(_get_user_info(user))


@user_blueprint.route("/user", methods=["POST"])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data["password"], method="sha256")

    new_user = User(
        public_id=str(uuid.uuid4()),
        username=data["username"].lower(),
        email=data["email"],
        password=hashed_password,
        admin=False,
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        return jsonify({"msg": "Failed to create user!"})

    requests.post('http://web:5005/addUser', json={"username": data["username"].lower()})

    return jsonify({"msg": "User created!"}), 200


@user_blueprint.route("/userFrontEnd", methods=["POST"])
def create_user_front_end():
    hashed_password = generate_password_hash(request.form["password"], method="sha256")

    new_user = User(
        public_id=str(uuid.uuid4()),
        username=request.form["username"].lower(),
        # email=data["email"],
        password=hashed_password,
        admin=False,
    )

    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception:
        return jsonify({"msg": "Failed to create user!"})

    requests.post('http://web:5005/addUser', json={"username": request.form["username"].lower()})

    return jsonify({"msg": "User " + request.form["username"] + " created!"}), 200


@user_blueprint.route("/user/<public_id>", methods=["DELETE"])
@admin_only
def delete_user(public_id):
    user = User.query.filter_by(public_id=public_id).first()

    if not user:
        return jsonify({"msg": "User not found!"})

    db.session.delete(user)
    db.session.commit()

    return jsonify({"msg": "User deleted!"})
