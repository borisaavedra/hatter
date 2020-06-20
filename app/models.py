from . import db

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    username = db.Column(db.String(200), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    avatar_url = db.Column(db.String(200), default="https://imgur.com/NVGmwQ4")
    bio = db.Column(db.String(200), default="I'm lazy so I don't have a bio... 😐")

    