from dataclasses import dataclass

@dataclass
class UserDomain:
    user_id: int
    username: str
    password: str
    bio: str