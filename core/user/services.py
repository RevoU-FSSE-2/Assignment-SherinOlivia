from injector import inject
from core.user.ports import IUserAccessor
from dotenv import load_dotenv

load_dotenv()

class UserService():
    
    @inject
    def __init__(self, user_accessor: IUserAccessor) -> None:
        self.user_accessor = user_accessor

    def get_by_id(self, user_id: int):
        user = self.user_accessor.get_by_id(user_id)

        if not user:
            return {"error message": "User not Found"}, 404

        return user

