from datetime import datetime, timedelta
from fastapi.param_functions import Depends

from jose import JWTError, jwt
from passlib.context import CryptContext

from models import UserInDB
import config


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(fake_db, username: str, password: str):
    user = get_user(fake_db, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_min: int = 15):
    settings = config.get_settings()
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=expires_min)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.jwt_secret_key, algorithm=settings.jwt_algorithm)

    return encoded_jwt
