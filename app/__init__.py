import os
from flask import Flask
from app.user.apis import user_blueprint
from app.auth.apis import auth_blueprint
# from app.tweet.apis import tweet_blueprint
from infrastructure.db import db, db_init
from app.common.bcrypt import bcrypt
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
database_url = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = database_url

db.init_app(app)
bcrypt.init_app(app)

# app.register_blueprint(tweet_blueprint, url_prefix="/tweet")
app.register_blueprint(auth_blueprint, url_prefix="/auth")
app.register_blueprint(user_blueprint)

with app.app_context():
    db_init()