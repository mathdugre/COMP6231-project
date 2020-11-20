from flask import jsonify, request, render_template
from app import redis_client
from app.redisCommands import redis_commands_blueprint  # noqa: E402, F401
import time
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

# class Post:
#     def __init__(self, user, topic, message, date):
#         self.user = user
#         self.topic = topic
#         self.message = message
#         self.date = date

# set of users
redis_sadd_users = "users"
# set of who user follows e.g. user1:follows
redis_sadd_user_follows = ":follows"
# set of followers, e.g. user1:followers
redis_sadd_user_followers = ":followers"
# key value of current post ID, is incremented after each post
redis_curr_post_key = "currPost"
# user posts, e.g. user1:posts
redis_list_user_posts = ":posts"
# list of post information, e.g. post:10
redis_list_post = "post:"


def userExists(username):
    return redis_client.sismember(redis_sadd_users, username)


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
    user_follow = data['tofollow']
    jwt_username = get_jwt_identity()['username']

    if not (userExists(user_follow) and userExists(user_request)):
        return jsonify({"msg:": "invalid, user(s) do not exist"}), 404

    if user_request != jwt_username:
        return jsonify({"msg:": "invalid, jwt token not for requesting user"}), 401

    if user_request == user_follow:
        return jsonify({"msg:": "invalid, you cannot follow yourself"}), 401

    if follow_user(user_request, user_follow):
        return jsonify({"msg": user_request + " now follows " + user_follow}), 200
    else:
        return jsonify({"msg": "unable to complete request. Either user already follows or internal error"}), 403


@redis_commands_blueprint.route("/unfollow", methods=["POST"])
@jwt_required
def unfollow():
    data = request.get_json()
    user_request = data['requester']
    user_unfollow = data['tounfollow']
    jwt_username = get_jwt_identity()['username']

    if not (userExists(user_unfollow) and userExists(user_request)):
        return jsonify({"msg:": "invalid, user(s) do not exist"}), 404

    if user_request != jwt_username:
        return jsonify({"msg:": "invalid, jwt token not for requesting user"}), 401

    if user_request == user_unfollow:
        return jsonify({"msg:": "invalid, you cannot follow yourself"}), 401

    if unfollow_user(user_request, user_unfollow):
        return jsonify({"msg": user_request + " now unfollows " + user_unfollow}), 200
    else:
        return jsonify(
            {"msg": "unable to complete request. Either user already does not follow or internal error"}), 403


def follow_user(user_request, user_follow):
    return (
            redis_client.sadd(user_request + redis_sadd_user_follows, user_follow) and
            redis_client.sadd(user_follow + redis_sadd_user_followers, user_request) == 1)


def unfollow_user(user_request, user_unfollow):
    return (
            redis_client.srem(user_request + redis_sadd_user_follows, user_unfollow) and
            redis_client.srem(user_unfollow + redis_sadd_user_followers, user_request) == 1)


@redis_commands_blueprint.route("/getallusers", methods=["GET"])
@jwt_required
def getAllUsers():
    userList = redis_client.smembers(redis_sadd_users)
    return jsonify(users=decodeRedisResp(userList), username=get_jwt_identity()['username'])


@redis_commands_blueprint.route("/getwhouserfollows", methods=["GET"])
@jwt_required
def getWhoUserFollows():
    username = request.args.get('username')
    jwt_username = get_jwt_identity()['username']

    if not userExists(username):
        return jsonify({"msg:": "invalid, user does not exist"}), 404
    if username != jwt_username:
        return jsonify({"msg:": "invalid, jwt token not for requesting user"}), 401

    userList = redis_client.smembers(username + redis_sadd_user_follows)
    return jsonify(users=decodeRedisResp(userList)), 200


@redis_commands_blueprint.route("/newpost", methods=["POST"])
@jwt_required
def newPost():
    username = get_jwt_identity()['username']
    topic = request.form['title']
    message = request.form['message']
    currtime = time.time()

    if topic == "" or message == "":
        return jsonify({"msg": "blank fields, invalid"}), 400

    if redis_client.exists(redis_curr_post_key):
        postID = redis_client.get(redis_curr_post_key).decode()
        redis_client.incr(redis_curr_post_key)
    else:
        postID = 1
        redis_client.set(redis_curr_post_key, 2)

    # push post to user
    redis_client.lpush(username + redis_list_user_posts, postID)
    redis_client.lpush(redis_list_post + str(postID), username, topic, message, currtime)

    # push post to followers
    followers = redis_client.smembers(username + redis_sadd_user_followers)
    followers = decodeRedisResp(followers)
    for follower in followers:
        redis_client.lpush(follower + redis_list_user_posts, postID)

    return jsonify({"msg": "post created", "username:": username, "topic": topic,
                    "message": message, "time": currtime}), 200


@redis_commands_blueprint.route("/getposts", methods=["GET"])
@jwt_required
def getPosts():
    username = get_jwt_identity()['username']
    post_Ids = redis_client.lrange(username + redis_list_user_posts, 0, -1)
    post_Ids = decodeRedisResp(post_Ids)
    posts = []

    for post_Id in post_Ids:
        post = redis_client.lrange(redis_list_post + str(post_Id), 0, -1)
        post = decodeRedisResp(post)
        for post_elem in post:
            posts.append(post_elem)

    return jsonify(posts), 200
