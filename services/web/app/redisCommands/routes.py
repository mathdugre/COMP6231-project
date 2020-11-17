from flask import jsonify, request, render_template
from app import redis_client
from app.redisCommands import redis_commands_blueprint  # noqa: E402, F401
import json
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

redis_sadd_users = "users"
redis_sadd_user_follows = ":follows"
redis_sadd_user_followers = ":followers"


def userExists(username):
    return redis_client.hexists(redis_sadd_users, username)


def decodeRedisResp(response):

    respList = list()
    for resp in response:
        respList.append(resp.decode())
    return respList


# TODO: there should be a secret key necessary to add a user
@redis_commands_blueprint.route("/addUser", methods=["POST"])
def addUser():
    data = request.get_json()
    username = data['username']

    if redis_client.sismember(redis_sadd_users, username):
        return jsonify({"msg:": "user already exists"}), 409

    redis_client.sadd(redis_sadd_users, username)

    return jsonify({"msg:": "user added"}), 200


@redis_commands_blueprint.route("/follow", methods=["POST"])
@jwt_required
def follow():
    data = request.get_json()
    user_request = data['requester']
    user_follow = data['follower']
    jwt_username = get_jwt_identity()['username']

    if not (userExists(user_follow) and userExists(user_request)):
        return jsonify({"msg:": "invalid, user(s) do not exist"}), 404

    if user_request != jwt_username:
        return jsonify({"msg:": "invalid, jwt token not for requesting user"}), 401

    if user_request == user_follow:
        return jsonify({"msg:": "invalid, you cannot follow yourself"}), 401

    if follow(user_request, user_follow):
        return jsonify({"msg": user_request + " now follows " + user_follow}), 200
    else:
        return jsonify({"msg": "unable to complete request. Either user already follows or internal error"}), 403


def follow(user_request, user_follow):
    return (
        redis_client.sadd(user_request + redis_sadd_user_follows, user_follow) and
        redis_client.sadd(user_follow + redis_sadd_user_followers, user_request) == 1)


@redis_commands_blueprint.route("/getallusers", methods=["GET"])
@jwt_required
def getAllUsers():
    userList = redis_client.smembers(redis_sadd_users)
    return jsonify(users=decodeRedisResp(userList), username=get_jwt_identity()['username'])



