import uuid

from flask.cli import FlaskGroup
from werkzeug.security import generate_password_hash

from app import app, db
from app.models import User


cli = FlaskGroup(app)


@cli.command("create_db")
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command("seed_db")
def seed_db():
    db.session.add(
        User(
            public_id=str(uuid.uuid4()),
            username="admin",
            email="foo@bar.com",
            password=generate_password_hash("admin"),
            admin=True,
        )
    )
    db.session.commit()


if __name__ == "__main__":
    cli()
