from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.responses import HTMLResponse
from starlette.requests import Request

from routers.sign.core import authenticate_user, create_access_token
from db import fake_users_db # TODO: temporary
from models import Token, User, UserInDB
from dependencies import get_current_user, templates
import config


router = APIRouter(
    prefix="/sign",
    tags=["sign"]
)


@router.get('/in', response_class=HTMLResponse)
async def sign_in(request: Request):
    return templates.TemplateResponse("sign_in.html", {"request": request})


@router.post('/in', response_model=Token)
async def sign_in(form_data: OAuth2PasswordRequestForm = Depends(), 
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
    token = Token(access_token=access_token, token_type='bearer')
    return token


@router.get('/test', response_model=User)
async def test(user: UserInDB = Depends(get_current_user)):
    return User(**user.dict())
