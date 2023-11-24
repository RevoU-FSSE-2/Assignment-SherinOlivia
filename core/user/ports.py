from abc import ABC, abstractmethod

class IUserAccessor(ABC):

    @abstractmethod
    def create(self, username: str, hashed_password: str, email: str, bio: str):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_username(self, username: str):
        raise NotImplementedError
    
    @abstractmethod
    def get_by_id(self, user_id: int):
        raise NotImplementedError