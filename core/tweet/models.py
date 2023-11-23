from dataclasses import dataclass
from datetime import datetime

@dataclass
class TweetDomain:
    id: int
    user_id: int
    tweet: str
    published_at: datetime