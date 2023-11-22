import os, jwt
from dotenv import load_dotenv

load_dotenv()

def decode_jwt(token):
    try:
        secret_key = os.getenv("SECRET_KEY")
        token_payload = jwt.decode(token, secret_key, algorithms="HS256")
        return token_payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None