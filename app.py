import os
from flask import Flask
from user.apis import user_blueprint
from db import db, db_init
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
database_url = os.getenv("DATABASE_URL")
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
db.init_app(app)

app.register_blueprint(user_blueprint)

with app.app_context():
    db_init()