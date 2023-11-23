import os, jwt
from flask import Blueprint, request
from infrastructure.user.models import User
from app.common.bcrypt import bcrypt
from datetime import datetime, timedelta
from dotenv import load_dotenv
from infrastructure.db import db
from marshmallow import Schema, fields, ValidationError
from core.auth.services import AuthService
from app.di import injector

load_dotenv()
auth_blueprint = Blueprint('auth', __name__)
auth_service = injector.get(AuthService)

class UserRegistrationSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)
    bio = fields.String(required=True)

@auth_blueprint.route('/registration', methods=['POST'])
def register_user():
    data = request.get_json()
    schema = UserRegistrationSchema()

    try:
        data = schema.load(data)
    except ValidationError as err:
        return {"error message": err.messages}, 400

    result = auth_service.register(
        username=data['username'],
        password=data['password'],
        bio=data['bio']
    )
    
    return result

class UserLoginSchema(Schema):
    username = fields.String(required=True)
    password = fields.String(required=True)

@auth_blueprint.route('/login', methods=['POST'])
def login_user():
    data = request.get_json()
    schema = UserLoginSchema()

    try:
        data = schema.load(data)
    except ValidationError as err:
        return {"error message": err.messages}, 400


    result = auth_service.login(
        username=data['username'],
        password=data['password']
    )

    if not result:
        return {"error_message": "Invalid Username/Password"}, 401

    # token_payload = {'user_id': result[0], 'exp': datetime.now() + timedelta(days=1)}
    # print("test result:", result[0])
    # secret_key = os.getenv("SECRET_KEY")
    # token = jwt.encode(token_payload, secret_key, algorithm='HS256')

    return result