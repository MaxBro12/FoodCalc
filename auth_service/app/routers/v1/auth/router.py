import logging
from fastapi import APIRouter, HTTPException, status, Response
from fastapi.requests import Request

from .models import UserLogin, UserRegister, TokenFull, AccessToken, UserName
from app.depends import DBDep
from core.pydantic_misc_models import Ok
from core.redis_client.dependency import RedisDep
from core.fast_decorators import cache
from core.security import SecurityService
from core.simplejwt import SimpleJWT
from core.trash import generate_trash_string

from app.settings import settings


auth_router_v1 = APIRouter(prefix='/v1/auth', tags=['auth'])


@auth_router_v1.post('/login', response_model=TokenFull)
@cache(key='login', expire=3600)
async def login(user_data: UserLogin, db: DBDep, redis: RedisDep):
    user = await db.users.check_password(user_data.name, user_data.password)
    if user:
        jwt = SimpleJWT(settings.AUTH_SECRET_KEY, settings.AUTH_ALGORITHM)
        uni = generate_trash_string(6)
        user.unique = uni
        return TokenFull(
            access_token=jwt.create_token({
                'uid': user.name,
            }, expire_delta=settings.AUTH_ACCESS_EXPIRE),
            refresh_token=jwt.create_token({
                'uid': user.name,
                'uni': user.unique
            }, expire_delta=settings.AUTH_REFRESH_EXPIRE_DAYS * 24 * 60 * 60)
        )
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail='Invalid user'
    )


@auth_router_v1.post('/refresh', response_model=AccessToken)
async def refresh(request: Request, response: Response):
    return {'ok': True}


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
