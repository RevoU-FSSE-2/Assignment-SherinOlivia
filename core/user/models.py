from dataclasses import dataclass

@dataclass
class UserDomain:
    id: int
    username: str
    email: str
    password: str
    bio: str