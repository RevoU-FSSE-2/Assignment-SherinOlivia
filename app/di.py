from injector import Injector
from infrastructure.user.modules import UserModule
from infrastructure.tweet.modules import TweetModule
from infrastructure.follow.modules import FollowModule

injector = Injector([
    UserModule,
    TweetModule,
    FollowModule
])