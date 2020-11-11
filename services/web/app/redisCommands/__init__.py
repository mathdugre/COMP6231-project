from flask import Blueprint

redis_commands_blueprint = Blueprint("redis_commands", __name__)

from app.redisCommands import routes  # noqa: E402, F401
