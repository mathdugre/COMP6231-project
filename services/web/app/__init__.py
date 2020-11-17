from flask import Flask, jsonify
from flask_jwt_extended import (JWTManager, jwt_required)
import redis

app = Flask(__name__)
app.config.from_object("app.config.Config")
redis_client = redis.Redis(host='redis', port=6379, db=0)
jwt = JWTManager(app)

from app.view import view_blueprint

app.register_blueprint(view_blueprint)

from app.redisCommands import redis_commands_blueprint

app.register_blueprint(redis_commands_blueprint)

if __name__ == "__main__":
    app.run()
