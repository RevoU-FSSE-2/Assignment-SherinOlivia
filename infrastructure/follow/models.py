from infrastructure.db import db

class Follow(db.Model):
    __tablename__ = 'follow'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_following = db.Column(db.Boolean, default=True, nullable=False)
    user = db.relationship('User',foreign_keys=[user_id], backref=db.backref('follower', lazy=True))
    target = db.relationship('User', foreign_keys=[target_id], backref=db.backref('following', lazy=True))