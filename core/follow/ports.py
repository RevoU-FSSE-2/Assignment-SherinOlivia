from abc import ABC, abstractmethod
from typing import Optional
from core.follow.models import FollowDomain

class IFollowAccessor(ABC):

    @abstractmethod
    def follow(self, user_id: int, target_id: int, is_following: bool):
        raise NotImplementedError

    def get_follow_relationship(self, user_id: int, target_id: int) -> Optional[FollowDomain]:
        raise NotImplementedError
    