from abc import ABC, abstractmethod
from datetime import datetime

class ITweetAccessor(ABC):

    @abstractmethod
    def create(self, tweet: str, user_id: int, published_at: datetime):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_user_id(self, user_id: str):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, tweet_id: int):
        raise NotImplementedError
