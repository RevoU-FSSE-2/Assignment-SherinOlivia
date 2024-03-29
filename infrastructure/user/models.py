from infrastructure.db import db

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(75), nullable=False)
    password = db.Column(db.String(100), nullable=False)
    bio = db.Column(db.String(200), nullable=False)