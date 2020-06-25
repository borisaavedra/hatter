from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password_hash = db.Column(db.String(200))
    avatar_url = db.Column(db.Text, default="https://simpleicon.com/wp-content/uploads/user1.png")
    bio = db.Column(db.String(200), default="I'm lazy so I don't have a bio... 😐")
    hatteses = db.relationship("Hattes", backref="users", lazy=True)
    relationses = db.relationship("Relations", backref="users", lazy=True)

    def __repr__(self):
        return '<Users %r>' % self.username

    @property
    def password(self):
        raise AttributeError("Password in not a readable attribute")

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self,  password):
        return check_password_hash(self.password_hash, password)


class Hattes(db.Model):
    __tablename__ = "hattes"
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(200), nullable=False)
    pic = db.Column(db.Text)
    created = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    status = db.Column(db.Integer, default=1)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __repr__(self):
        return '<Hattes %r>' % self.id


class Relations(db.Model):
    __tablename__ = "relations"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    followed_id = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return '<Relations %r>' % self.id

class Codes(db.Model):
    __tablename__ = "codes"
    id = db.Column(db.Integer, primary_key=True)
    code_name = db.Column(db.String(200), nullable=False)
    status = db.Column(db.Integer, default=1)

    def __repr__(self):
        return '<Codes %r>' % self.id





    