from flask_bcrypt import Bcrypt
from db import db

bcrypt = Bcrypt()

class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(200), nullable=False)