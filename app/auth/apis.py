from flask import Blueprint, request
from datetime import datetime, timedelta
from marshmallow import Schema, fields, ValidationError
from core.auth.services import AuthService
from app.di import injector

auth_blueprint = Blueprint('auth', __name__)
auth_service = injector.get(AuthService)

class UserRegistrationSchema(Schema):
    username = fields.String(required=True)
    email = fields.Email(required=True)
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
        email=data['email'],
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

    return result