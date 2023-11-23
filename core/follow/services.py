import os, jwt
from injector import inject
from core.follow.ports import IFollowAccessor
from core.auth.ports import IUserAccessor

class FollowService():

    @inject
    def __init__(self, follow_accessor: IFollowAccessor, user_accessor: IUserAccessor) -> None:
        self.follow_accessor = follow_accessor
        self.user_accessor = user_accessor

    def follow(self, user_id: int, target_id: int, is_following: bool):
        follow_domain = self.follow_accessor.follow(user_id=user_id, target_id=target_id, is_following=is_following)

        existing_follow = self.follow_accessor.get_follow_relationship(user_id, target_id)
        user_domain = self.user_accessor.get_by_id(user_id)
        target_user_domain = self.user_accessor.get_by_id(target_id)

        if user_id == target_id:
            return {"error_message": "Can't follow yourself!!"}, 400
        
        if existing_follow.is_following == False:
            return {
            "message": f"{user_domain.username} unfollowed {target_user_domain.username}"
            }, 200
        elif existing_follow.is_following == True:
            return {
            "message": f"{user_domain.username} started following {target_user_domain.username}"
            }, 200
