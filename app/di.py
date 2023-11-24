from injector import Injector
from infrastructure.user.modules import UserModule
from infrastructure.tweet.modules import TweetModule
from infrastructure.follow.modules import FollowModule
from infrastructure.auth.modules import HashingModule

injector = Injector([
    UserModule,
    TweetModule,
    FollowModule,
    HashingModule
])