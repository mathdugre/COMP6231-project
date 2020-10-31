from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


app = Flask(__name__)
app.config.from_object("app.config.Config")

db = SQLAlchemy(app)
jwt = JWTManager(app)

from app.jwt import jwt_blueprint  # noqa: E402

app.register_blueprint(jwt_blueprint)

from app.user import user_blueprint  # noqa: E402

app.register_blueprint(user_blueprint)


if __name__ == "__main__":
    app.run()
