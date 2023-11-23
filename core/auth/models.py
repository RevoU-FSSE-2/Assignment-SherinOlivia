from dataclasses import dataclass

@dataclass
class UserDomain:
    id: int
    username: str
    password: str
    bio: str