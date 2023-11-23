from dataclasses import dataclass

@dataclass
class FollowDomain:
    id: int
    user_id: int
    target_id: int
    is_following: bool