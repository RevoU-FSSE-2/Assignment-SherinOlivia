from core.auth.models import UserDomain
from core.common.utils import ObjectMapperUtil
from core.auth.ports import IUserAccessor
from infrastructure.db import db
from infrastructure.user.models import User

class UserAccessor(IUserAccessor):

    def create(self, username: str, bio: str, hashed_password: str):
        new_user = User(username=username, bio=bio, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return ObjectMapperUtil.map(new_user, UserDomain)

        
    def get_by_username(self, username: str):
        user = User.query.filter_by(username=username).first()
        return ObjectMapperUtil.map(user, UserDomain)
    
    def get_by_id(self, user_id: int):
        user = User.query.get(user_id)
        return ObjectMapperUtil.map(user, UserDomain)