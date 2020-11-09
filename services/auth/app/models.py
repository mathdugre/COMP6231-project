from app import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(50), unique=True, nullable=False)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=True)
    password = db.Column(db.String(128), nullable=False)
    admin = db.Column(db.Boolean)

    def __repr__(self) -> str:
        return f"<User {self.public_id}>"
