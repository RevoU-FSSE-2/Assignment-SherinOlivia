from core.follow.models import FollowDomain
from core.common.utils import ObjectMapperUtil
from core.follow.ports import IFollowAccessor
from infrastructure.db import db
from infrastructure.follow.models import Follow
from typing import Optional

class FollowAccessor(IFollowAccessor):

    def follow(self, user_id: int, target_id: int, is_following: bool):
        existing_follow = self.get_follow_relationship(user_id, target_id)

        if existing_follow:
            existing_follow.is_following = not existing_follow.is_following
            db.session.commit()
            
            return ObjectMapperUtil.map(existing_follow, FollowDomain)

        else:    
            new_follow = Follow(user_id=user_id, target_id=target_id, is_following=is_following)
            db.session.add(new_follow)      
            db.session.commit()

            return ObjectMapperUtil.map(new_follow, FollowDomain)

    def get_follow_relationship(self, user_id: int, target_id: int) -> Optional[FollowDomain]:
        return Follow.query.filter_by(user_id=user_id, target_id=target_id).first()