import os
import jwt
from flask import Blueprint, request
from tweet.models import Tweet
from user.models import User
from tweet.constants import TWEET_DATE_FORMAT
from datetime import datetime, timedelta
from dotenv import load_dotenv
from db import db

load_dotenv()
tweet_blueprint = Blueprint('tweet', __name__)

@tweet_blueprint_route('', methods=['POST'])
def create_tweet():
    token = request.headers.get('Authorization')
    data = request.get_json()
    tweet = data["tweet"]

    if len(tweet) > 150:
        return {"error_message": "Tweet tidak boleh lebih dari 150 karakter"}, 400

    if not token:
        return {"error_message": "Token tidak valid"}, 401
    
    secret_key = os.getenv("SECRET_KEY")
    print("Token: ", token)
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])

    user_id = decoded_token['user_id']
    
    user = User.query.filter_by(user_id=user_id).first()

    if not user:
        return {"error_message": "User unavailable"}, 404
    
    new_tweet = Tweet(tweet=tweet, published_at=datetime.now().strftime(TWEET_DATE_FORMAT), user=user)
    db.session.add(new_tweet)
    db.session.commit()

    return {
        'id': new_tweet.id,
        'published_at': new_tweet.published_at,
        "tweet": new_tweet.tweet
    }, 200
    
@tweet_blueprint_route('', methods=['GET'])
def get_tweet():
    token = request.headers.get('Authorization')

    if not token:
        return {"error_message": "Token tidak valid"}, 401
    
    secret_key = os.getenv("SECRET_KEY")
    print("Token: ", token)
    decoded_token = jwt.decode(token, secret_key, algorithms=['HS256'])

    user_id = decoded_token['user_id']
    
    user = User.query.filter_by(user_id=user_id).first()

    tweets = Tweet.query.filter_by(user=user).all()

    if user:
        list_of_tweet = []
        for tweet in tweets:
            tweet_data = {
                'id': tweet.id,
                'published_at': tweet.published_at,
                'tweet': tweet.tweet
            }
            list_of_tweet.append(tweet_data)
        
        if len(list_of_tweet) == 0:
            return {"error_message": "Tweets Unavailable"}, 404

        return {"tweets": list_of_tweet}