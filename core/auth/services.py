import os, jwt
from injector import inject
from core.auth.ports import IUserAccessor
from app.common.bcrypt import bcrypt
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

class AuthService():

    @inject
    def __init__(self, user_accessor: IUserAccessor) -> None:
        self.user_accessor = user_accessor

    def register(self, username: str, password: str, bio: str):
        hashed_password = bcrypt.generate_password_hash(password).decode('UTF-8')
        existing_user = self.user_accessor.get_by_username(username=username)

        if existing_user.username is not None:
            return {"error message": "username already taken" }, 400

        user_domain = self.user_accessor.create(
            username=username,
            hashed_password=hashed_password,
            bio=bio
        )

        return {
            'user_id': user_domain.id,
            "username": user_domain.username,
            "bio": user_domain.bio
        }, 200

    def login(self, username: str, password: str):
        valid_user = self.user_accessor.get_by_username(username=username)
        if not valid_user:
            return {"error_message": "Invalid Username/Password"}, 401

        valid_password = bcrypt.check_password_hash(valid_user.password, password)
        if not valid_password:
            return {"error_message": "Invalid Username/Password"}, 401
        
        token_payload = {'user_id': valid_user.id, 'exp': datetime.now() + timedelta(days=1)}
        secret_key = os.getenv("SECRET_KEY")
        token = jwt.encode(token_payload, secret_key, algorithm='HS256')

        return {'token': token}, 200


        