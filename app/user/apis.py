from flask import Blueprint, request
from core.user.services import UserService
from infrastructure.tweet.models import Tweet
from infrastructure.follow.models import Follow
from infrastructure.user.models import User
from app.auth.utils import decode_jwt
from app.di import injector

user_blueprint = Blueprint('user', __name__)
user_service = injector.get(UserService)

@user_blueprint.route('', methods=['GET'])
def get_user():
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)
    if not token_payload:
        return {"error_message": "Invalid Token"}, 401

    user_id = token_payload['user_id']

    user = user_service.get_by_id(user_id)

    if not user:
        return {"error_message": "User not Found"}, 404

    tweets = Tweet.query.filter_by(user_id=user_id).order_by(Tweet.published_at.desc()).limit(10).all()

    list_of_tweets = []
    for tweet in tweets:
        tweet_data = {
            'id': tweet.id,
            'tweet': tweet.tweet,
            'published_at': tweet.published_at
        }
        list_of_tweets.append(tweet_data)

    follower_count = Follow.query.filter_by(target_id=user_id, is_following=True).count()
    if Follow.query.filter_by(target_id=user_id).count() > 0:
        follower_count = follower_count
    else:
        follower_count = 0

    following_count = Follow.query.filter_by(user_id=user_id, is_following=True).count()
    if Follow.query.filter_by(user_id=user_id).count() > 0:
        following_count = following_count
    else:
        following_count = 0

    return {
        'user_id': user.id,
        'username': user.username,
        'email': user.email,
        'bio': user.bio,
        'follower': follower_count,
        'following': following_count,
        'tweets': list_of_tweets
    }, 200

@user_blueprint.route('/feed', methods=['GET'])
def get_user_feed():
    token = request.headers.get('Authorization')
    token_payload = decode_jwt(token)

    if not token_payload:
        return {"error_message": "Invalid Token"}, 401

    user_id = token_payload['user_id']

    user = user_service.get_by_id(user_id)

    if not user:
        return {"error_message": "User not Found"}, 404

    check_following = Follow.query.filter_by(user_id=user_id, is_following=True).count()
    if check_following > 0:
        following_tweets = (
            Tweet.query
            .join(Follow, Follow.target_id == Tweet.user_id) # Tweet table join with Follow table
            .join(User, User.id == Tweet.user_id) # Tweet table join with User table too
            .filter(Follow.user_id == user_id, Follow.is_following == True)
            .order_by(Tweet.published_at.desc())
            .limit(20).all()
        )
    else:
        following_tweets = (
            Tweet.query
            .join(User, User.id == Tweet.user_id) # Tweet table only join with User table cause not following anyone
            .filter(Tweet.user_id == user_id)
            .order_by(Tweet.published_at.desc())
            .limit(10).all()
        )

    list_of_tweets = []
    for following_tweet in following_tweets:
        tweet_data = {
            'id': following_tweet.id,
            'user_id': following_tweet.user_id,
            'username': following_tweet.user.username,
            'tweet': following_tweet.tweet,
            'published_at': following_tweet.published_at
        }
        list_of_tweets.append(tweet_data)

    return {
        'tweets': list_of_tweets
    }, 200