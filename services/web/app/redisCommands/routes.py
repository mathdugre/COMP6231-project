from io import BytesIO
from flask import jsonify, request, send_file
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
redis_set_users = "users"
# set of who user follows e.g. user1:follows
redis_set_user_follows = ":follows"
# set of followers, e.g. user1:followers
redis_set_user_followers = ":followers"
# key value of current post ID, is incremented after each post
redis_curr_post_key = "currPost"
# user posts, e.g. user1:posts
redis_list_user_posts = ":posts"
# list of post information, e.g. post:10
redis_list_post = "post:"
# list of file information: user_uploader, data
redis_list_file = "file:"
# set of user files
redis_set_user_files = ":files"
# set of filenames which exist
redis_set_files = "filenames"

def userExists(username):
    return redis_client.sismember(redis_set_users, username)


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

    if redis_client.sismember(redis_set_users, username):
        return jsonify({"msg:": "user already exists"}), 409

    redis_client.sadd(redis_set_users, username)

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
            redis_client.sadd(user_request + redis_set_user_follows, user_follow) and
            redis_client.sadd(user_follow + redis_set_user_followers, user_request) == 1)


def unfollow_user(user_request, user_unfollow):
    return (
            redis_client.srem(user_request + redis_set_user_follows, user_unfollow) and
            redis_client.srem(user_unfollow + redis_set_user_followers, user_request) == 1)


@redis_commands_blueprint.route("/getallusers", methods=["GET"])
@jwt_required
def getAllUsers():
    userList = redis_client.smembers(redis_set_users)
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

    userList = redis_client.smembers(username + redis_set_user_follows)
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
    followers = redis_client.smembers(username + redis_set_user_followers)
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


@redis_commands_blueprint.route("/upload", methods=["POST"])
@jwt_required
def upload():
    file = request.files['fileUpload']
    data = file.read()
    file_name = file.filename
    username = get_jwt_identity()['username']

    if file_name == "":
        return jsonify({"msg": "file name is empty"}), 400

    if redis_client.exists(redis_list_file + file_name):
        return jsonify({"msg": "file with same name already exists"}), 400

    redis_client.lpush(redis_list_file + file_name, data, username)
    redis_client.sadd(redis_set_files, file_name)
    redis_client.sadd(username+redis_set_user_files, file_name)

    return jsonify({"msg": "uploaded " + file_name + " successfully"}), 200


@redis_commands_blueprint.route("/getfilenames", methods=["GET"])
@jwt_required
def getfiles():
    username = get_jwt_identity()['username']

    file_names = redis_client.smembers(redis_set_files)
    user_files = redis_client.smembers(username + redis_set_user_files)
    file_names = decodeRedisResp(file_names)
    user_files = decodeRedisResp(user_files)

    return jsonify({"allFiles": file_names, "userFiles": user_files})


@redis_commands_blueprint.route("/download", methods=["GET"])
@jwt_required
def download():
    file_name = request.args.get('filename')

    if not redis_client.sismember(redis_set_files, file_name):
        return jsonify({"msg": "file does not exist"}), 400

    file_data = redis_client.lindex(redis_list_file + file_name, 1)

    return send_file(BytesIO(file_data), attachment_filename=file_name, as_attachment=True), 200


@redis_commands_blueprint.route("/deletefile", methods=["GET"])
@jwt_required
def deleteFile():
    file_name = request.args.get('filename')
    username = get_jwt_identity()['username']

    if not redis_client.sismember(redis_set_files, file_name):
        return jsonify({"msg": "file does not exist"}), 400

    file_owner = redis_client.lindex(redis_list_file+file_name, 0).decode()

    if username != file_owner:
        return jsonify({"msg": "file does not belong to user"}), 400

    redis_client.delete(redis_list_file + file_name)
    redis_client.srem(username+redis_set_user_files, file_name)
    redis_client.srem(redis_set_files, file_name)

    return jsonify({"msg": file_name + " deleted"}), 200

