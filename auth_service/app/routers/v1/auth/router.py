import logging
from fastapi import APIRouter, HTTPException, status, Response
from fastapi.requests import Request

from .models import UserLogin, UserRegister, TokenFull, AccessToken, RefreshToken, UserName
from app.depends import DBDep
from app.handlers.auth import auth_handler
from core.pydantic_misc_models import Ok
from core.redis_client.dependency import RedisDep
from core.fast_decorators import cache
from core.security import SecurityService
from core.simplejwt import SimpleJWT
from core.trash import generate_trash_string

from app.settings import settings


auth_router_v1 = APIRouter(prefix='/v1/auth', tags=['auth'])


@auth_router_v1.post('/login', response_model=TokenFull)
async def login(user_data: UserLogin, db: DBDep):
    user = await db.users.check_password(user_data.name, user_data.password)
    if user:
        return auth_handler.create_tokens(user)
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Invalid user'
    )


@auth_router_v1.post('/refresh', response_model=TokenFull)
async def refresh(token: RefreshToken, db: DBDep):
    token_data = auth_handler.verify_refresh_token(token.refresh_token)
    if token_data is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token'
        )
    user = await db.users.by_id(token_data.payload['usp'])
    if user is None or user.name != token_data.payload['uid'] \
    or user.unique != token_data.payload['uni']:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    return auth_handler.create_tokens(user)


@auth_router_v1.post('/logout', response_model=Ok)
async def logout(db: DBDep, user_data: UserName):
    user = await db.users.by_name(user_data.name)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='User not found'
        )
    await db.users.clear_uni(user.id)
    return {'ok': True}


@auth_router_v1.post('/register', response_model=Ok)
async def register(user_data: UserRegister, db: DBDep):
    if len(user_data.name) < 6 or len(user_data.password) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Логин или пароль должны быть больше 6")
    if await db.users.exists(user_data.name):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Имя пользователя уже существует")
    if not await db.keys.exists(user_data.key):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ввели неправильный ключ")

    key = await db.keys.by_hash(user_data.key)
    if key is None or not await db.users.new(
        username=user_data.name,
        password=SecurityService.hash(user_data.password),
        is_admin=False,
        key_id=key.id,
    ):
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Внутренняя ошибка приложения, свяжитесь с администрацией"
        )
    return {'ok': True}
