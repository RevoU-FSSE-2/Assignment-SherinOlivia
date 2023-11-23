import os
from flask import Blueprint, request
from core.user.services import UserService
from infrastructure.user.models import User
from app.auth.utils import decode_jwt
from app.di import injector
# from datetime import datetime, timedelta

user_blueprint = Blueprint('user', __name__)
user_service = injector.get(UserService)

@user_blueprint.route('/user', methods=['GET'])
def get_user():
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)

    if not token_payload:
        return {"error_message": "Invalid Token"}, 401

    user_id = token_payload['user_id']
    print('user_id:', user_id)

    user = user_service.get_by_id(user_id)

    if not user:
        return {"error_message": "User not Found"}, 404

    return {
        'user_id': user.id,
        'username': user.username,
        'bio': user.bio
    }, 200