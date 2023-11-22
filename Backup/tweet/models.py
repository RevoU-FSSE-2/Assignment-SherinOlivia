from db import db

class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    published_at = db.Column(db.DateTime, nullable=False)
    tweet = db.Column(db.String(150), nullable=False)
    user = db.relationship('User', backref=db.backref('tweets', lazy=True))

