import os
from flask import Blueprint, request
from user.models import User, bcrypt
import jwt
from datetime import datetime, timedelta
from db import db
from dotenv import load_dotenv

load_dotenv()
user_blueprint = Blueprint('user', __name__)

@user_blueprint.route('/auth/registration', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data["username"]
    password = data["password"]
    bio = data["bio"]

    # check for username:
    existing_username = User.query.filter_by(username=username).first()
    if existing_username:
        return {"error_message": "username sudah digunakan"}, 400

    hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')

    new_user = User(username=username, password=hashed_password, bio=bio)
    db.session.add(new_user)
    db.session.commit()

    return {
        'user_id': new_user.user_id,
        "username": new_user.username,
        "bio": new_user.bio
    }, 200

@user_blueprint.route('/auth/login', methods=['POST'])
def login_user():
    data = request.get_json()
    username = data["username"]
    password = data["password"]

    user = User.query.filter_by(username=username).first()

    if user and bcrypt.check_password_hash(user.password, password):
        token_payload = {'user_id': user.user_id, 'exp': datetime.now() + timedelta(days=1)}
        secret_key = os.getenv("SECRET_KEY")
        token = jwt.encode(token_payload, secret_key, algorithm='HS256')

        return {'token': token}, 200

    return {"error_message": "username atau password tidak tepat"}, 401

@user_blueprint.route('/user', methods=['GET'])
def get_user():
    token = request.headers.get('Authorization')

    if not token:
        return {"error_message": "Token tidak valid"}, 401
    
    secret_key = os.getenv("SECRET_KEY")
    print("Token: ", token)
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])

    user_id = decoded_token['user_id']
    
    user = User.query.filter_by(user_id=user_id).first()

    if user:
        return {
            'user_id': user.user_id,
            'username': user.username,
            'bio': user.bio
        }, 200