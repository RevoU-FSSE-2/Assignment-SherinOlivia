from flask import Blueprint, request
from core.tweet.services import TweetService
from core.user.services import UserService
from infrastructure.tweet.constants import TWEET_DATE_FORMAT
from app.auth.utils import decode_jwt
from app.di import injector
from datetime import datetime, timedelta
from marshmallow import Schema, fields, ValidationError

tweet_blueprint = Blueprint('tweet', __name__)
tweet_service = injector.get(TweetService)
user_service = injector.get(UserService)

class CreateTweetSchema(Schema):
    tweet = fields.String(required=True)

@tweet_blueprint.route('', methods=['POST'])
def create_tweet():
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)
    
    if not token_payload:
        return {"error_message": "Invalid Token"}, 401

    user_id = token_payload['user_id']

    user = user_service.get_by_id(user_id)

    if not user:
        return {"error_message": "User not Found"}, 404

    data = request.get_json()
    schema = CreateTweetSchema()

    try:
        data = schema.load(data)
    except ValidationError as err:
        return {"error message": err.messages}, 400

    if len(data['tweet']) > 150:
        return {"error_message": "Tweet Can't be longer than 150 characters"}, 400

    result = tweet_service.create(
        tweet=data['tweet'],
        user_id=user_id,
        published_at = data.get('published_at', datetime.utcnow().strftime(TWEET_DATE_FORMAT))
    )

    return result