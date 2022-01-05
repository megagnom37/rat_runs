from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from fastapi.templating import Jinja2Templates
from jose import jwt, JWTError

import config
from routers.sign.core import get_user
from db import fake_users_db # TODO: temporary


templates = Jinja2Templates(directory="static/templates")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/sign/in")


async def get_current_user(token: str = Depends(oauth2_scheme),
                           settings: config.Settings = Depends(config.get_settings)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.jwt_secret_key, algorithms=[settings.jwt_algorithm])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = get_user(fake_users_db, username=username)
    if user is None:
        raise credentials_exception
    return user


