from core.tweet.models import TweetDomain
# from core.auth.models import UserDomain
from core.common.utils import ObjectMapperUtil
from core.tweet.ports import ITweetAccessor
from infrastructure.db import db
from infrastructure.tweet.models import Tweet
from infrastructure.user.models import User
from infrastructure.tweet.constants import TWEET_DATE_FORMAT
from datetime import datetime

class TweetAccessor(ITweetAccessor):

    def create(self, tweet: str, user_id: int, published_at: datetime):
        user = User.query.get(user_id)
        new_tweet = Tweet(user_id=user.id, tweet=tweet, published_at=datetime.now().strftime(TWEET_DATE_FORMAT))
        db.session.add(new_tweet)
        db.session.commit()

        return ObjectMapperUtil.map(new_tweet, TweetDomain)

    def get_by_user_id(self, user_id: str):
        user = User.query.get(user_id)
        tweets = Tweet.query.filter_by(user_id=user.id).all()

        return [ObjectMapperUtil.map(tweet, TweetDomain) for tweet in tweets]
    
    def get_by_id(self, tweet_id: int):
        tweet = Tweet.query.get(tweet_id)
        return ObjectMapperUtil.map(tweet, TweetDomain)