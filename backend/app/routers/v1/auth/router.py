import logging
from random import randint

from fastapi import APIRouter, HTTPException, status

from .models import Token, UserLogin, UserRegister
from app.routers.misc_models import Ok
from app.depends import SessionDep
from app.database import DB
from app.core.auth import verify_hashed, create_access_token, get_hash
from app.core.trash import generate_trash_string


auth_router_v1 = APIRouter(prefix='/v1/auth', tags=['auth'])


@auth_router_v1.post('/login', response_model=Token | Ok)
async def login(user_data: UserLogin, session: SessionDep):
    logging.info(f'login > {user_data.username}')
    user = await DB.users.by_name(get_hash(user_data.username), session)
    if not user or not verify_hashed(user_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Некорректное имя пользователя или пароль",
        )
    return {
        "access_token": create_access_token(data={
            "sub": user.name,
            generate_trash_string(randint(3, 6)): generate_trash_string(randint(5, 20))
        }),
        "token_type": "bearer"
    }


@auth_router_v1.post('/register', response_model=Ok)
async def register(user_data: UserRegister, session: SessionDep):
    logging.info(f'register > {user_data.username} - {user_data.key}')
    if len(user_data.username) < 6 or len(user_data.password) < 6:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Логин или пароль должны быть больше 6")
    if await DB.users.exists(user_data.username, session):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Имя пользователя уже существует")
    if not await DB.keys.exists(user_data.key, session):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Ввели неправильный ключ")

    key = await DB.keys.by_hash(user_data.key, session)
    if key is None or not await DB.users.new(get_hash(user_data.username), get_hash(user_data.password), key.id, session):
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Внутренняя ошибка приложения, свяжитесь с администрацией")
    return {'ok': True}
