import os, jwt
from injector import inject
from core.tweet.ports import ITweetAccessor
from core.auth.ports import IUserAccessor
from datetime import datetime, timedelta

class TweetService():

    @inject
    def __init__(self, tweet_accessor: ITweetAccessor, user_accessor: IUserAccessor) -> None:
        self.tweet_accessor = tweet_accessor
        self.user_accessor = user_accessor

    def create(self, tweet: str, user_id: int, published_at: datetime):
        tweet_domain = self.tweet_accessor.create(tweet=tweet, user_id=user_id, published_at=published_at)
        user_domain = self.user_accessor.get_by_id(user_id)

        if len(tweet) > 150:
            return {"error_message": "Tweet Can't be longer than 150 characters"}, 400
        
        return {
            'user_id': user_domain.id,
            "username": user_domain.username,
            "tweet": tweet_domain.tweet,
            "published_at": tweet_domain.published_at
        }, 200