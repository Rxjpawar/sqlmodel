import bcrypt
from datetime import timedelta
from config import settings
import jwt
def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))

def create_access_token(user_data:dict,expiry:timedelta):
    payload={}
    token = jwt.emcode(
        payload = payload,
        key = settings.JWT_SECRET,
        alorithm=settings.JWT_ALGORITHM)