from flask import Blueprint, request
from core.follow.services import FollowService
from core.user.services import UserService
from infrastructure.follow.models import Follow
from app.auth.utils import decode_jwt
from app.di import injector
from marshmallow import Schema, fields, ValidationError

follow_blueprint = Blueprint('follow', __name__)
follow_service = injector.get(FollowService)
user_service = injector.get(UserService)

class FollowSchema(Schema):
    target_id = fields.Int(required=True)

@follow_blueprint.route('', methods=['POST'])
def follow():
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)
    if not token_payload:
        return {"error_message": "Invalid Token"}, 401

    user_id = token_payload['user_id']
    user = user_service.get_by_id(user_id)

    if not user:
        return {"error_message": "User not Found"}, 404

    data = request.get_json()
    schema = FollowSchema()

    try:
        data = schema.load(data)
    except ValidationError as err:
        return {"error message": err.messages}, 400

    # is_following = (
    #     Follow.query
    #     .filter_by(user_id=user.id, target_id=data['target_id'], is_following=True)
    #     .first() is not None
    # )
    # print('is_following:', is_following)

    already_follow = Follow.query.filter_by(user_id=user.id, target_id=data['target_id']).first()

    if already_follow:
        is_following = False
    else:
        is_following = True
        
    result = follow_service.follow(
        user_id=user.id,
        target_id=data['target_id'],
        is_following=is_following
    )

    return result