from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from routers.sign.core import authenticate_user, create_access_token
from models import Token
import config


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/sign/in")


# TODO: temporary solution
fake_users_db = {
    "megagnom37": {
        "username": "megagnom37",
        "email": "megagnom37@gmail.com",
        "hashed_password": "$2b$12$EixZaYVK1fsbw1ZfbX3OXePaWxn96p36WQoeG6Lruj3vjPGga31lW",
        "disabled": False,
    }
}


router = APIRouter(
    prefix="/sign",
    tags=["sign"]
)


@router.post('/in', response_model=Token)
def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), 
            settings: config.Settings = Depends(config.get_settings)):
    user = authenticate_user(fake_users_db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(
        data={"sub": user.username}, expires_min=settings.token_expire_min
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get('/test')
def test(token: str = Depends(oauth2_scheme)):
    return {'token': token}