from fastapi import APIRouter, HTTPException, status, Response
from fastapi.requests import Request

from .models import UserLogin, UserRegister
from app.routers.misc_models import Ok
from app.depends import DBDep, AuthDep, TokenDep
from app.core_old.auth import AuthService
from app.core_old.base import verify_hashed, get_hash
from app.core_old.debug import logger


auth_router_v1 = APIRouter(prefix='/v1/auth', tags=['auth'])


@auth_router_v1.post('/login', response_model=Ok)
async def login(response: Response, user_data: UserLogin, db: DBDep, auth: AuthDep):
    user = await db.users.by_name(user_data.username)
    if not user or not verify_hashed(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_406_NOT_ACCEPTABLE,
            detail="Некорректное имя пользователя или пароль",
        )
    await auth.create_tokens(user=user, response=response)
    return {'ok': True}


@auth_router_v1.post('/refresh', response_model=Ok)
async def refresh(request: Request, response: Response, auth: AuthDep):
    await auth.refresh(request=request, response=response)
    return {'ok': True}


@auth_router_v1.post('/logout', response_model=Ok)
async def logout(request: Request, response: Response, auth: AuthDep):
    data = await auth.verify_access_token(request)
    await auth.logout(user_id=data.user.id, response=response)
    return {'ok': True}


@auth_router_v1.post('/register', response_model=Ok)
async def register(user_data: UserRegister, db: DBDep):
    logger.info(f'register > {user_data.username} - {user_data.key}')
    if len(user_data.username) < 6 or len(user_data.password) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Логин или пароль должны быть больше 6")
    if await db.users.exists(user_data.username):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Имя пользователя уже существует")
    if not await db.keys.exists(user_data.key):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ввели неправильный ключ")

    key = await db.keys.by_hash(user_data.key)
    if key is None or not await db.users.new(
        username=user_data.username,
        password=get_hash(user_data.password),
        is_admin=key.is_admin,
        key_id=key.id,
    ):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка приложения, свяжитесь с администрацией")
    return {'ok': True}


@auth_router_v1.post('/authorized')
async def test(request: Request, response: Response, token: TokenDep):
    return {"ok": True}
