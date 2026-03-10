import bcrypt
from datetime import timedelta
from config import settings
import jwt
from datetime import datetime
from uuid import UUID, uuid4
import logging
ACCESS_TOKEN_EXPIRY = 3600

def generate_password_hash(password: str) -> str:
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)
    return hashed.decode("utf-8")

def verify_password(password: str, hash: str) -> bool:
    return bcrypt.checkpw(password.encode("utf-8"), hash.encode("utf-8"))

def create_access_token(user_data:dict,expiry:timedelta = None,refresh:bool = False):
    payload={}
    payload["user"]=user_data
    payload["exp"]= datetime.now()+ (expiry if expiry is not None else timedelta(seconds=ACCESS_TOKEN_EXPIRY))
    payload["jti"]=str(uuid4())
    payload["refresh"]=refresh
    token = jwt.encode(
        payload = payload,
        key = settings.JWT_SECRET,
        algorithm=settings.JWT_ALGORITHM)
    return token

def decode_token(token:str)->dict:
    try:
        token_data=jwt.decode(
            jwt=token,
            key = settings.JWT_SECRET,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return token_data
    except jwt.PyJWTError as e:
        logging.exception(e)
        return None